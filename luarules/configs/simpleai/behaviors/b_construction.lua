--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--
--  file:    luarules/configs/simpleai/behaviors/b_construction.lua
--  brief:   Construction behavior for the SimpleAI gadget (TA:Recoil port of
--           Splinter Faction's). Owns the entire economy-building brain: the
--           priority-chain project selector, factory queues, constructor
--           self-preservation, and every related tunable.
--
--           TA:Recoil changes: no supply cap (the unit limit stands in);
--           storage is per resource; metal makers are the energy->metal sink
--           (built when energy brims and switched off in an energy stall);
--           mex spots take whichever extractor fits them (land / underwater),
--           basic mexes are upgraded to mohos in place; builders repair,
--           finish nanoframes and assist factories; sea buildings are only
--           offered near water; every pick is cost-gated against income.
--
--           Registers services.SelectConstructionProject so other behaviors
--           (the commander) can request "build something sensible here" —
--           this module must therefore appear BEFORE b_commander in the
--           core's BEHAVIOR_FILES manifest.
--
--           Owns ctx state: ctx.pacing.factoryDelay / constructorDelay /
--           lastConStart / lastFacStart; increments ctx.counters.converters
--           optimistically on order.
--           Reads: ctx.intel.airThreat + ctx.IsAATurret + ctx.counters.
--           aaTurrets for the reactive anti-air rung (priority 5a).
--
--           Storage growth (priority 5s): raises team storage toward
--           STOR.GOAL over the game, one project at a time. All
--           stock-ratio thresholds in the chain are measured against the
--           signal pool (cfg.SignalPool, owned by the core), not raw
--           storage, so a big bank does not make the AI hoard.
--
--           Stall response: reads ctx.stall (core). While a team is
--           stalling, factory queues are kept short and no new factories
--           are started; while it is stalling on ENERGY, factories lean
--           toward energy-cheap units and no constructors are queued.
--           (Pausing and cancelling factory work is b_throttle's job.)
--
--           Power plant sizing (GeneratorPick): the plant that best fits
--           the energy shortfall, counting plants already on order.
--           Factory count (facRoom): tied to metal income, and none added
--           while the throttle has recently had to pause one.
--
--           Reachability (lib.Reachable): building sites, bricks, factory
--           sites, metal spots, vents, forward turret sites and reclaim
--           fields are all checked with the engine's pathfinder, so nothing
--           is ordered somewhere it cannot be walked to from home.
--
--           Commander leash (BASE.CommLeash): a commander only builds,
--           takes metal spots and uses vents within its leash of home.
--
--           Base layout (BASE): economy buildings go into bricks behind
--           home (lib.BrickOrder), factories and support buildings are
--           sited around home, and only builders near home do base work.
--
--           Builder safety (SAFE / Hostile): every rung that sends a
--           builder away from the base (far mex spots, reclaim, forward
--           turrets) first checks the destination and the walk to it for
--           armed enemies.
--
--           Reclaim (REC, rungs R and P12): a scanned field of wrecks, a
--           crew of builders sized to it, targeted area-reclaim orders,
--           and extra constructors when the field is rich.
--
--           Forward defense (FWD, rung 5f): a few turrets at the team's
--           most forward extractors and muster point, facing the enemy.
--
--           Herd control (JOB): caps how many builders may answer the
--           same need at once (generators, turrets), recounted from real
--           command queues each team tick.
--
--           Decision trace: every project selection is tallied by rung
--           into ctx.trace[teamID]; the core publishes it for the game
--           recorder widget. Rung labels match the PRIORITY comments.
--
--  license: GNU GPL, v2 or later
--
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

return function(ctx, lib, cfg, services)

	--------------------------------------------------------------------------
	-- Tunables (owned by this behavior)
	--------------------------------------------------------------------------
	-- Constructor caps
	local CONSTRUCTOR_MAX         = 8   -- max constructors for normal AI teams
	local CONSTRUCTOR_MAX_CON_AI  = 14  -- higher cap for dedicated SimpleConstructorAI teams
	-- Minimum frames between STARTING any new constructor on a team. Because every
	-- factory on a team is evaluated in the same GameFrame tick, without this they
	-- all read the same stale count and queue a constructor at once. This rate-limit
	-- lets the count catch up so the hard cap is actually respected.
	local CON_BUILD_SPACING      = 150  -- ~5s at 30Hz

	-- Higher-tier preference. Per-unit build weight scales with (techTier+1)^bias,
	-- so advanced units/factories are chosen far more often while lower tiers still appear.
	local TECH_UNIT_BIAS    = 1.8    -- combat unit tech preference
	local TECH_FAC_BIAS     = 2.4    -- factory tech preference (want advanced plants to unlock advanced units)

	-- Turret demand model
	local TURRET_BASE        = 2     -- always want at least this many turrets once a factory exists
	local TURRET_PER_FAC     = 1     -- + this many wanted per factory
	local TURRET_PER_MEX_DIV = 3     -- + 1 wanted per this many mexes
	local TURRET_CAP         = 20    -- absolute max turrets to build per team

	-- Anti-air demand model. ctx.intel.airThreat[teamID] carries the frame of
	-- the last enemy-aircraft evidence (armed air spotted inside the base scan
	-- in b_defense, or ANY of our units damaged by enemy air, stamped by the
	-- core). While that stamp is fresh, builders raise DEDICATED AA turrets
	-- toward the count below -- a reactive rung that jumps the queue like the
	-- generic under-attack turret slot, because against bombers a random
	-- ground turret is a dead spend. AA turrets are a subset of IsTurret, so
	-- they also count toward TURRET_CAP and the generic desired-turret model.
	local AA_THREAT_MEMORY   = 1800  -- frames the last air evidence stays "fresh" (~60s)
	local AA_BASE            = 2     -- AA turrets wanted while the threat is fresh...
	local AA_PER_FAC_DIV     = 2     -- ...+1 per this many factories
	local AA_CAP             = 6     -- absolute max AA from this reactive model

	local MEX_TARGET_EARLY  = 3      -- grab this many mexes before anything else
	local MEX_TARGET_MID    = 14     -- expand to this many once economy is running
	local MEX_RANGE_EARLY   = 3500   -- mex search radius before the first factory
	local MEX_RANGE_MID     = 5000   -- mex search radius once we have 2+ factories
	local MEX_UPGRADE_RANGE = 3500   -- how far a builder goes to put a moho on a mex
	local CONVERTER_BASE    = 2      -- metal makers: this many, plus one per CONVERTER_PER_E of energy income
	local CONVERTER_PER_E   = 120
	local CONVERTER_MAX     = 16
	local FACTORY_MAX       = 8      -- max factories per team
	local LAND_FAC_MIN      = 1      -- build at least this many land factories before any air/sea
	local AFFORD_SECS       = 120    -- a pick may cost this many seconds of metal income plus the bank...
	local AFFORD_FAC_SECS   = 300    -- ...factories this many
	local REPAIR_BELOW      = 0.70   -- builders repair friendly units under this health fraction
	local REPAIR_R          = 1600   -- ...within this of themselves
	local ASSIST_R          = 1200   -- builders finish nanoframes / assist factories within this
	-- Factory build pacing. A flat frame-based limiter (like the constructor one),
	-- so the Nth factory is no slower to start than the 2nd. When resources are
	-- overflowing we build them much faster, since extra production capacity is
	-- the best sink for a surplus.
	local FACTORY_SPACING       = 90   -- normal min frames between starting factories (~3s)
	local FACTORY_SPACING_FLOOD = 45   -- min frames when overflowing (~1.5s)

	-- Storage growth model. The AI used to finish every game on the stock
	-- 1k/1k pool, which late-game income fills and drains inside one AI
	-- tick. It now grows storage steadily toward STOR.GOAL:
	--   wanted = the larger of the tech floor below and
	--            STOR.INCOME_SECS seconds of the bigger income,
	--            capped at the tech ceiling below
	-- and, if both stocks are brimming against REAL storage, it heads for
	-- the tech ceiling right away regardless of the schedule.
	-- Storage per tech: smallstorage (200) at tech 1, mediumstorage (2000)
	-- at tech 2, largestorage (20000) at tech 3. The ceilings keep the AI
	-- from chasing a late-game number with early-game buildings.
	-- One storage project per team at a time, at least STOR.SPACING
	-- frames apart, so the climb is gradual and never eats the economy.
	-- Kept in one table (with the per-team pacing state below) because the
	-- project selector is at Lua 5.1's 60-upvalue limit.
	local STOR = {
		-- TA: energy storage 3000 for 240 metal, metal storage 1000 for 305. The
		-- schedule is per resource: wanted = INCOME_SECS of that income, at least
		-- the tech floor, at most the tech ceiling; brimming takes the ceiling.
		GOAL        = 60000,
		TECH_FLOOR  = { m = { [1] = 1000, [2] = 2000, [3] = 4000 }, e = { [1] = 1000, [2] = 7000, [3] = 16000 } },
		TECH_CEIL   = { m = { [1] = 3000, [2] = 6000, [3] = 20000 }, e = { [1] = 7000, [2] = 13000, [3] = 25000 } },
		INCOME_SECS_M = 90,   -- seconds of metal income the bank should hold
		INCOME_SECS_E = 10,   -- seconds of energy income (the D-Gun alone wants 400)
		MIN_MEXES     = 6,    -- no storage before this many mexes (a TA opening spends its metal on mexes and a factory)
		MAX_STEPS   = 20,     -- ignore a storage size that would need more than this many buildings to close the gap
		DEBUG       = cfg.TRACE_ECHO or false,   -- echo storage decisions to infolog
		boOk = 0, boFail = 0, geoOk = 0, geoFail = 0, -- placements since the last project selection (see SimpleBuildOrder)
		stallV = ctx.stall and ctx.stall.v or {},   -- [teamID] = combined stall 0..1 (core-owned, see ctx.stall)
		stallE = ctx.stall and ctx.stall.e or {},   -- [teamID] = energy stall 0..1
		STALL_ON = cfg.STALL_ON or 0.20,            -- stalling threshold (core-owned)
		STALL_QUEUE = 2,                            -- factory queue depth while stalling (normally 10)
		-- Power plant sizing (see GeneratorPick): build the plant that fits the shortfall.
		GEN_HEADROOM  = 1.25,                       -- cover the shortfall with this much to spare
		GEN_OVERSHOOT = 1.5,                        -- a plant may exceed the need by this factor, no more
		GEN_MAX_STEP  = 2.0,                        -- believe a shortfall of at most this many times current income...
		GEN_STEP_FLOOR = 500,                       -- ...plus this (E/s), per decision
		GEN_GROWTH    = 0.50,                       -- with no measurable shortfall, grow income by this share (TA: T1 plants are 20-30 E each)
		GEN_MIN       = 60,                         -- ...and never plan for less than this (E/s)
		GEN_COST_SECS = 150,                        -- a plant may cost this many seconds of metal income, plus what is banked
		-- Factory count (see facRoom): production capacity the economy can actually feed.
		FAC_BASE         = 1,                       -- factories every team may have
		FAC_INCOME_EACH  = 7,                       -- one more per this much metal income (M/s): a TA T1 lab eats ~7 M/s flat out
		FAC_PAUSE_MEMORY = 3600,                    -- no new factory within this many frames of one being paused (~2 min)
		lastPaused       = {},                      -- [teamID] = last frame the throttle had a factory on WAIT
		reachLogged = {},                           -- [teamID] = frame the reachability totals were last logged
		stallPaused = ctx.stall and ctx.stall.paused or {},   -- [teamID] = factories on WAIT now (b_throttle)
		SUPPORT_BASE = 1, SUPPORT_PER_FAC = 4, SUPPORT_MAX = 2,   -- per-type cap on misc buildings (radar, targeting...): 1 + one per 4 factories, at most 2
		support = {},                               -- [defID] = true for misc buildings (the "building" category)
		STALL_CON_FLOOR = 4,                        -- an energy stall never holds the team below this many constructors
		CON_EMERGENCY = 2,                          -- below this many, a factory queues one even at the supply cap
		STALL_COST_POWER = 4,                       -- how hard a stall pushes factories toward cheap units
		dbgAt       = {},     -- [teamID] = next frame a "why not" line may be echoed
		trace       = ctx.trace or {},  -- [teamID] = { [rungKey] = count } decision tallies (core-owned, see ctx.trace)
		BRIM        = 0.88,   -- a stock above this fraction of REAL storage = brimming
		SPACING     = 900,    -- min frames between storage starts (~30s)
		PENDING_MAX = 3600,   -- give up waiting on an unfinished storage after this (~120s)
		RETRY       = 150,    -- back-off after a failed placement (~5s)
		COST_SECS   = 150,    -- prefer storage costing at most this many seconds of metal income
		FIT         = 1.5,    -- do not pick a storage bigger than this x the remaining gap

		-- defID-keyed, filled at load
		cap  = {},            -- [defID] = storage capacity (the larger of its metal and energy)
		capM = {}, capE = {}, -- [defID] = metal / energy storage it adds
		cost = {},            -- [defID] = metal cost
		-- per-team pacing state (owned here, not shared through ctx)
		lastStart = {},       -- [teamID] = frame the last storage was ordered
		pending   = {},       -- [teamID] = frame a storage was ordered and has not finished
		retryAt   = {},       -- [teamID] = earliest frame to try again after a failed placement
	}

	-- Metal maker switching (TA: makers burn 60 E for 1 M; the first thing a
	-- player turns off in an energy stall). [teamID] = true while ours are off.
	local MM = { off = {}, OFF_AT = 0.15, ON_AT = 0.60 }

	-- Herd control. A need like "energy is low" does not go away until the
	-- thing built for it FINISHES, so every idle builder used to see the same
	-- need and answer it at once: seven builders on seven fusion plants, all
	-- splitting the same energy, none finishing. (Assisting is a rung of its own
	-- here, "AS"; every builder on a build rung is a separate building.)
	-- JOB tracks which builders are currently working for which need and
	-- caps how many may answer it at the same time. A builder past the cap
	-- falls through to the next rung instead. The ledger is recounted from
	-- the builders' real command queues every team tick, so a builder that
	-- died, finished, fled or was re-tasked stops counting on its own.
	-- (Supply and storage have their own on-order accounting above; factories
	-- and constructors are spaced by their frame limiters.)
	local JOB = {
		MAX = {
			gen = 3,   -- generators / converters under way at once (rungs P2, P7, MM)
			tur = 2,   -- turrets under way at once (rungs 5a, 5b, 5f, 6b, P13)
			rep = 2,   -- builders repairing (rung REP)
			as  = 4,   -- builders finishing nanoframes or assisting factories (rungs AS, FB)
			-- (the reclaim crew, need "rec", is sized per team by the field: REC.slots)
		},
		RUNG = { P2 = "gen", P7 = "gen", MM = "gen", ["5a"] = "tur", ["5b"] = "tur", ["5f"] = "tur", ["6b"] = "tur", P13 = "tur", R = "rec",
		         REP = "rep", AS = "as", ["FB.assist"] = "as" },
		of     = {},   -- [teamID] = { [unitID] = need } builders currently on a capped need
		active = {},   -- [teamID] = { gen = n, tur = n } recounted every team tick
	}

	-- Income targets required to trigger each tech upgrade.
	-- Key = current tech level. Values are the income thresholds to AIM for.
	-- (TA: a metal spot gives ~2 M/s, a solar 20 E, a fusion 1000 E.)
	local TECH_INCOME_GOALS = {
		[1] = { m = 14,  e = 350  },
		[2] = { m = 35,  e = 1500 },
		[3] = { m = 70,  e = 4000 },
	}

	-- How strongly to bias toward economy when below the tech threshold.
	-- 0.5 = balanced: economy prioritised but army still builds.
	local TECH_ECONOMY_BIAS = 0.5

	--------------------------------------------------------------------------
	-- Shared state / config
	--------------------------------------------------------------------------
	local mapsizeX          = cfg.mapsizeX
	local mapsizeZ          = cfg.mapsizeZ
	local FACTORY_OVERFLOW  = cfg.FACTORY_OVERFLOW
	local SignalPool        = cfg.SignalPool
	local IsAirFactory      = ctx.IsAirFactory or {}
	local IsSeaFactory      = ctx.IsSeaFactory or {}
	local IsAssistant       = ctx.IsAssistant or {}
	local TierOf            = ctx.Tier or {}

	local IsFactory     = ctx.IsFactory
	local IsConstructor = ctx.IsConstructor

	local SimpleFactoriesCount   = ctx.counters.factories
	local SimpleT1Mexes          = ctx.counters.mexes
	local SimpleConstructorCount = ctx.counters.constructors
	local SimpleConverterCount   = ctx.counters.converters
	local SimpleTurretCount      = ctx.counters.turrets
	local SimpleAATurretCount    = ctx.counters.aaTurrets
	local SimpleLandFacCount     = ctx.counters.landFactories
	local IsAATurret             = ctx.IsAATurret
	local SimpleAirThreat        = ctx.intel.airThreat
	local SimpleFactoryDelay     = ctx.pacing.factoryDelay
	local SimpleConstructorDelay = ctx.pacing.constructorDelay
	local SimpleLastConStart     = ctx.pacing.lastConStart
	local SimpleLastFacStart     = ctx.pacing.lastFacStart
	local SimpleUnderAttack      = ctx.intel.underAttack
	local SimpleEnemyBasePos     = ctx.intel.enemyBase
	local TeamTechLevel          = ctx.techLevel
	local IsExtractor            = ctx.IsExtractor or {}

	local GetBuildable            = lib.GetBuildable
	local GetBuildableTechBiased  = lib.GetBuildableTechBiased
	local GetWeightedBuildable    = lib.GetWeightedBuildable
	local CombatRoleWeight        = lib.CombatRoleWeight
	local FindMexSpot             = lib.FindMexSpot
	local FindMexUpgrade          = lib.FindMexUpgrade
	local EnergyOutput            = lib.EnergyOutput
	-- Geothermal placement. Buildings that need a vent (the condenser, the
	-- geothermal power plant, the geo metal maker) cannot go through the
	-- normal "next to a friendly building" search: the engine only accepts
	-- them ON a vent, and that search never lands on one except by luck. For
	-- a long time that is exactly what happened: the condenser is tagged as
	-- storage, outbid the real storage buildings, and then failed to place
	-- ~98% of the time, which is why the AI built no storage at all.
	-- Now any needGeo def is sent to the nearest free vent instead.
	local GEO = {
		RANGE = 3500,     -- how far a builder will walk to a vent (elmos)
		NEAR  = 1200,     -- ...the commander, or anyone before the first factory, only this far
		HOME_RANGE = 4500, -- and never to a vent farther than this from the team's start
		CLAIM = 1800,     -- frames a vent stays reserved for the builder sent to it (~60s)
		need  = {},       -- [defID] = true for needGeo defs
		spots = nil,      -- cached vent positions { {x=,y=,z=}, ... }; built on first use
		claim = {},       -- [spotIndex] = frame the reservation expires
		why   = "none",   -- why the last search found nothing: none (no vents on the map) | far | taken | unsafe | unreach
	}
	for defID, ud in pairs(UnitDefs) do
		if ud.needGeo then GEO.need[defID] = true end
	end

	-- Nearest vent within GEO.RANGE of the builder that is unreserved and that
	-- the engine will accept this def on right now (so a vent that already
	-- carries a building is skipped). Returns spotIndex, spot or nil.
	local function GeoSpotFor(unitID, project)
		if not GEO.spots then
			if Spring.GetGameFrame() < 1 then return nil end   -- vents not final yet
			-- Two sources, merged: the vents game_geovent_spots.lua publishes
			-- (game rules params), and the map's geothermal features.
			local spots = {}
			local function Add(x, z)
				for i = 1, #spots do
					local dx, dz = spots[i].x - x, spots[i].z - z
					if dx * dx + dz * dz < 64 * 64 then return end
				end
				spots[#spots + 1] = { x = x, y = Spring.GetGroundHeight(x, z), z = z }
			end
			for i = 1, (Spring.GetGameRulesParam("customGeovent_count") or 0) do
				local x = Spring.GetGameRulesParam("customGeovent_" .. i .. "_x")
				local z = Spring.GetGameRulesParam("customGeovent_" .. i .. "_z")
				if x and z then Add(x, z) end
			end
			local features = Spring.GetAllFeatures()
			for i = 1, #features do
				local fDef = FeatureDefs[Spring.GetFeatureDefID(features[i])]
				if fDef and fDef.geoThermal then
					local x, _, z = Spring.GetFeaturePosition(features[i])
					if x then Add(x, z) end
				end
			end
			GEO.spots = spots
			Spring.Echo("[SimpleAI] geothermal vents known to the AI: " .. #spots)
		end
		GEO.why = (#GEO.spots == 0) and "none" or "far"
		local ux, _, uz = Spring.GetUnitPosition(unitID)
		if not ux then return nil end
		local teamID = Spring.GetUnitTeam(unitID)
		local now = Spring.GetGameFrame()

		-- How far this unit may go for a vent. A recorded 1v1 was lost in the
		-- opening because the commander walked 3,700 elmos to a mid-map vent
		-- before the team had a factory (first factory at 4:09 against the
		-- opponent's 1:23). So: the commander never leaves the base for a
		-- vent, and nobody does before the first factory is up.
		local reach = GEO.RANGE
		local isCommander = ctx.IsCommander and ctx.IsCommander[Spring.GetUnitDefID(unitID) or 0]
		if isCommander or (SimpleFactoriesCount[teamID] or 0) == 0 then
			reach = GEO.NEAR
		end
		-- ...and the vent itself must be within GEO.HOME_RANGE of home, so a
		-- builder already far forward does not chain on to the enemy's side.
		local home  = STOR.HomeOf and STOR.HomeOf(teamID)
		local home2 = GEO.HOME_RANGE * GEO.HOME_RANGE

		local bestI, bestD = nil, reach * reach
		for i = 1, #GEO.spots do
			local s = GEO.spots[i]
			local dx, dz = s.x - ux, s.z - uz
			local d = dx * dx + dz * dz
			local nearHome = true
			if home then
				local hdx, hdz = s.x - home.x, s.z - home.z
				local d2 = hdx * hdx + hdz * hdz
				nearHome = d2 <= home2
				if isCommander then
					local leash = STOR.BASE.CommLeash(teamID, unitID) or GEO.NEAR
					nearHome = nearHome and d2 <= leash * leash
				end
			end
			if d < bestD and nearHome then
				if now < (GEO.claim[i] or 0)
						or Spring.TestBuildOrder(project, s.x, s.y, s.z, 0) ~= 2 then
					GEO.why = "taken"    -- a vent in reach, but reserved, built on or blocked
				elseif STOR.Hostile and STOR.Hostile(teamID, ux, uz, s.x, s.z) then
					GEO.why = "unsafe"   -- armed enemies at the vent or on the way
				elseif lib.Reachable and not lib.Reachable(teamID, Spring.GetUnitDefID(unitID), s.x, s.z) then
					GEO.why = "unreach"  -- no way to walk there from home
				else
					bestI, bestD = i, d
				end
			end
		end
		if bestI then return bestI, GEO.spots[bestI] end
		return nil
	end

	-- Base layout. A recorded game ended with three allied bases smeared over
	-- three quarters of the map: every building was placed next to wherever
	-- its builder happened to be standing, and builders wander. Now the base
	-- is laid out the way a player does it (see the brick planner in lib.lua):
	-- economy in tight bricks behind home, factories around home, and base
	-- work is done by builders who are near home.
	local BASE = {
		brickCat = { generator = true, converter = true, storage = true, supply = true },
		homeCat  = { factory = true },
		RANGE    = 3500,   -- a builder farther than this from home leaves base work to others
		COMM_LEASH = 1800, -- default commander leash if the commander behavior has not set one
	}
	-- How far from home this unit may build: a number for a commander, nil
	-- (no limit) for anything else.
	function BASE.CommLeash(teamID, unitID)
		local defID = Spring.GetUnitDefID(unitID)
		if not (defID and ctx.IsCommander and ctx.IsCommander[defID]) then return nil end
		local set = ctx.comm and ctx.comm.leash
		return (set and set[teamID]) or BASE.COMM_LEASH
	end
	STOR.BASE  = BASE
	STOR.brick = {}       -- brick planner outcomes since the last project selection (for the trace)

	-- Every placement goes through here: vent buildings to a vent, everything
	-- else to the normal search. It also counts hits and misses so the
	-- decision trace can report them ("bo" / "bo!", and for vent placements
	-- "geo" / "geo!.none" / "geo!.far" / "geo!.taken" / "geo!.unsafe").
	local function SimpleBuildOrder(unitID, project)
		if STOR.DEBUG and IsFactory[project] then
			local q = Spring.GetCommandQueue(unitID, 0)
			Spring.Echo(("[SimpleAI] team %d %s orders factory %s (queue %d, frame %d)"):format(Spring.GetUnitTeam(unitID),
				UnitDefs[Spring.GetUnitDefID(unitID)].name, UnitDefs[project].name, q or -1, Spring.GetGameFrame()))
		end
		if GEO.need[project] then
			local i, s = GeoSpotFor(unitID, project)
			if i then
				Spring.GiveOrderToUnit(unitID, -project, { s.x, s.y, s.z, 0 }, { "shift" })
				GEO.claim[i] = Spring.GetGameFrame() + GEO.CLAIM
				STOR.geoOk = STOR.geoOk + 1
				return true
			end
			STOR.geoFail = STOR.geoFail + 1
			STOR.geoWhy  = GEO.why
			return false
		end
		-- Base layout. Where a building goes depends on what it is:
		--   economy (power, converters, storage, supply) -> a slot in one of
		--     the team's bricks behind the base (lib.BrickOrder)
		--   factories and support buildings -> the lane-keeping search, but
		--     outward from HOME, not from wherever the builder is standing
		--   everything else (turrets) -> the lane-keeping search around the
		--     builder, as before
		local teamID = Spring.GetUnitTeam(unitID)
		local home   = teamID and STOR.HomeOf(teamID)
		local cat    = ctx.defCat and ctx.defCat[project]
		-- The commander builds only within its leash of home (set by the
		-- commander behavior; see BASE.CommLeash). Everything farther out
		-- is engineers' work.
		local leash  = home and BASE.CommLeash(teamID, unitID)
		if home and BASE.brickCat[cat] then
			local enemy = SimpleEnemyBasePos[teamID]
			local ok = lib.BrickOrder(unitID, project, teamID, home.x, home.z, enemy and enemy.x, enemy and enemy.z, leash)
			STOR.brick[lib.brickResult] = (STOR.brick[lib.brickResult] or 0) + 1
			if ok then
				STOR.boOk = STOR.boOk + 1
				return true
			end
			-- No brick could be planned anywhere in range (very cramped
			-- start), or the free slots are beyond this builder's leash (the
			-- commander): fall back to the search around home so the team is
			-- not left without power or storage.
			if lib.brickResult ~= "exhausted" and lib.brickResult ~= "leash" then
				STOR.boFail = STOR.boFail + 1
				return false
			end
		end
		local ox, oz
		if home and (leash or BASE.homeCat[cat] or BASE.brickCat[cat] or STOR.support[project]) then
			ox, oz = home.x, home.z
		end
		if lib.BuildOrder(unitID, project, ox, oz, leash) then
			STOR.boOk = STOR.boOk + 1
			return true
		end
		STOR.boFail = STOR.boFail + 1
		return false
	end
	STOR.GeoSpotFor = GeoSpotFor   -- the storage pick asks "is there a vent for this builder?"
	STOR.geo        = GEO.need

	-- Builder safety. A recorded 28-minute game lost 9 engineers a minute
	-- across six teams, nearly every one of them thousands of elmos from
	-- home: builders were being sent to far mex spots, wrecks and forward
	-- sites with no look at what stood in the way. Hostile() answers "would
	-- this trip take a builder under enemy guns?": armed enemy units near the
	-- destination, or near the straight line to it. Every rung that sends a
	-- builder away from the base asks first. (The AI already reads enemy
	-- positions directly elsewhere; this is no new information.)
	local SAFE = {
		RADIUS = 700,   -- armed enemies within this of a checked point make it unsafe
		STEP   = 900,   -- check a point every this many elmos along the way
		MAX    = 6,     -- most points checked per trip (destination first)
		ALERT  = 800,   -- a builder reacts to enemies within this range of itself
		FLEE_REISSUE = 150,   -- frames between flee orders for one builder (~5s)
		fleeAt = {},    -- [unitID] = frame the next flee order may be given
		STUCK      = 900,   -- frames a builder may hold a build order without moving or building (~30s)
		STUCK_MOVE = 64,    -- moving less than this in that time counts as not moving
		watch  = {},    -- [unitID] = { x=, z=, since= } stuck-builder watchdog
	}
	local function ArmedEnemyNear(teamID, x, z)
		local nearby = Spring.GetUnitsInCylinder(x, z, SAFE.RADIUS)
		for i = 1, #nearby do
			local other = Spring.GetUnitTeam(nearby[i])
			if other and other ~= teamID and not Spring.AreTeamsAllied(teamID, other) then
				local ud = UnitDefs[Spring.GetUnitDefID(nearby[i]) or 0]
				if ud and ud.weapons and #ud.weapons > 0 then return true end
			end
		end
		return false
	end
	local function Hostile(teamID, fromX, fromZ, toX, toZ)
		if ArmedEnemyNear(teamID, toX, toZ) then return true end
		local dx, dz = toX - fromX, toZ - fromZ
		local dist = math.sqrt(dx * dx + dz * dz)
		local steps = math.min(SAFE.MAX - 1, math.floor(dist / SAFE.STEP))
		-- walk back from the destination; the builder's own position is not
		-- checked (if enemies are on top of it, its flee logic is already running)
		for i = 1, steps do
			local f = 1 - i / (steps + 1)
			if ArmedEnemyNear(teamID, fromX + dx * f, fromZ + dz * f) then return true end
		end
		return false
	end
	STOR.Hostile = Hostile

	-- Forward defense. Ordinary turret rungs build next to whatever friendly
	-- building the builder happens to be near, which means the base. This
	-- puts a FEW turrets where the team actually meets the enemy:
	--   * candidate sites are the team's own extractors and its army muster
	--     point, i.e. ground it already holds;
	--   * a site only counts as forward if it is clearly closer to the enemy
	--     than the team's start position (FWD.ADVANCE);
	--   * only the FWD.SITES most forward sites are considered, each gets at
	--     most FWD.PER_SITE turrets within FWD.COVER of it.
	-- So the total is small and it follows the frontier as the team expands
	-- or is pushed back. Turrets go on the enemy-facing side of the site.
	local FWD = {
		SITES    = 3,      -- how many of the most forward sites get defended
		PER_SITE = { 1, 2, 2, 2 },   -- turrets per site, by tech level
		COVER    = 500,    -- a turret within this many elmos of a site defends it
		ADVANCE  = 0.15,   -- site must be this much closer to the enemy than home is
		SPACING  = 900,    -- min frames between forward turret starts per team (~30s)
		CLAIM    = 2700,   -- a site ordered but not yet started counts as covered this long (~90s)
		last     = {},     -- [teamID] = frame of the last forward order
		claim    = {},     -- [teamID] = { x=, z=, untilFrame= } site a builder is walking to
	}
	-- A team's home: where its first commander appeared (owned by the core,
	-- ctx.home). Deliberately not Spring.GetTeamStartPosition, which in SF
	-- can be thousands of elmos from where the team actually starts.
	-- nil until the commander exists.
	local teamHome = ctx.home or {}
	function STOR.HomeOf(teamID)
		return teamHome[teamID]
	end
	local IsExtractorDef = ctx.IsExtractor or {}
	local IsTurretDef    = ctx.IsTurret or {}
	local fwdSites, fwdTurX, fwdTurZ = {}, {}, {}   -- scratch

	-- Find the most forward under-defended site and order `unitID` to build a
	-- turret there. Returns true if an order went out. `units` is the team's
	-- unit list, `turretDefs` the non-AA turrets this builder can make.
	local function ForwardTurretOrder(unitID, teamID, units, turretDefs, techLevel, now)
		local enemy = SimpleEnemyBasePos[teamID]
		if not enemy or #turretDefs == 0 then return false end

		local home = STOR.HomeOf(teamID)
		if not home then return false end
		local hdx, hdz = enemy.x - home.x, enemy.z - home.z
		local homeDist = math.sqrt(hdx * hdx + hdz * hdz)
		if homeDist < 1 then return false end
		local maxDist = homeDist * (1 - FWD.ADVANCE)

		-- One pass over the team: forward extractors become sites, turrets
		-- (finished or not) are remembered for the coverage count.
		local nSites, nTur = 0, 0
		local function AddSite(x, z)
			local dx, dz = enemy.x - x, enemy.z - z
			local d = math.sqrt(dx * dx + dz * dz)
			if d <= maxDist then
				nSites = nSites + 1
				local s = fwdSites[nSites]
				if not s then s = {}; fwdSites[nSites] = s end
				s.x, s.z, s.d = x, z, d
			end
		end
		for i = 1, #units do
			local defID = Spring.GetUnitDefID(units[i])
			if defID then
				if IsExtractorDef[defID] then
					local x, _, z = Spring.GetUnitPosition(units[i])
					if x then AddSite(x, z) end
				elseif IsTurretDef[defID] then
					local x, _, z = Spring.GetUnitPosition(units[i])
					if x then nTur = nTur + 1; fwdTurX[nTur], fwdTurZ[nTur] = x, z end
				end
			end
		end
		local muster = ctx.squad and ctx.squad.muster and ctx.squad.muster[teamID]
		if muster and muster.x then AddSite(muster.x, muster.z) end
		if nSites == 0 then return false end

		local claim = FWD.claim[teamID]
		if claim and now < claim.untilFrame then
			nTur = nTur + 1; fwdTurX[nTur], fwdTurZ[nTur] = claim.x, claim.z
		end

		-- Walk the sites from most forward; stop at the first one short of
		-- its turret allowance. Selection-style pick of the next-closest site
		-- keeps this allocation-free (sites are few).
		local allowance = FWD.PER_SITE[techLevel] or 2
		local cover2    = FWD.COVER * FWD.COVER
		local pick
		for rank = 1, math.min(FWD.SITES, nSites) do
			local bi, bd = nil, math.huge
			for i = 1, nSites do
				local s = fwdSites[i]
				if s.d < bd then bi, bd = i, s.d end
			end
			local s = fwdSites[bi]
			local covered = 0
			for t = 1, nTur do
				local dx, dz = fwdTurX[t] - s.x, fwdTurZ[t] - s.z
				if dx * dx + dz * dz <= cover2 then covered = covered + 1 end
			end
			if covered < allowance then pick = s; break end
			s.d = math.huge   -- fully defended: look at the next most forward
		end
		if not pick then return false end
		-- not if the walk there, or the site itself, is under enemy guns
		local ux, _, uz = Spring.GetUnitPosition(unitID)
		if not ux or Hostile(teamID, ux, uz, pick.x, pick.z) then return false end
		-- ...and not if the builder cannot walk there at all
		if lib.Reachable and not lib.Reachable(teamID, Spring.GetUnitDefID(unitID), pick.x, pick.z) then return false end

		-- Place it on the enemy-facing side of the site: straight toward the
		-- enemy first, then fanning out to either side, then further away.
		local ex, ez = enemy.x - pick.x, enemy.z - pick.z
		local el = math.sqrt(ex * ex + ez * ez)
		ex, ez = ex / el, ez / el
		local turretDef = turretDefs[math.random(1, #turretDefs)]
		for ring = 1, 3 do
			local r = 110 + ring * 70
			for step = 0, 4 do
				for side = -1, 1, 2 do
					if step > 0 or side < 0 then
						local a  = side * step * 0.45
						local ca, sa = math.cos(a), math.sin(a)
						local bx = pick.x + (ex * ca - ez * sa) * r
						local bz = pick.z + (ex * sa + ez * ca) * r
						if bx > 128 and bz > 128 and bx < mapsizeX - 128 and bz < mapsizeZ - 128 then
							local by = Spring.GetGroundHeight(bx, bz)
							if Spring.TestBuildOrder(turretDef, bx, by, bz, 0) == 2
									and #Spring.GetUnitsInRectangle(bx - 48, bz - 48, bx + 48, bz + 48) == 0 then
								Spring.GiveOrderToUnit(unitID, -turretDef, { bx, by, bz, 0 }, { "shift" })
								FWD.last[teamID]  = now
								FWD.claim[teamID] = { x = pick.x, z = pick.z, untilFrame = now + FWD.CLAIM }
								return true
							end
						end
					end
				end
			end
		end
		return false
	end
	STOR.Forward = ForwardTurretOrder
	STOR.FWD     = FWD

	-- Reclaim. Wrecks are a large part of SF's economy and the AI used to
	-- ignore them: its one reclaim rung sat at the bottom of the chain and sent
	-- a builder to area-reclaim around the ENEMY base. This is the replacement:
	--   * FIELD: every REC.SCAN frames all reclaimable features are binned
	--     into a coarse grid (metal per cell, metal-weighted center). One scan
	--     serves every AI team.
	--   * CREW: a team keeps up to REC.MAX builders on reclaim, one per
	--     REC.PER_BUILDER metal within reach of home, never more than half its
	--     constructors (herd control, need "rec").
	--   * TARGET: a crew builder is sent to area-reclaim the best cell in its
	--     reach: most metal for the walk, not already taken by a teammate, and
	--     not sitting under enemy guns.
	--   * BUILDERS: when the field near home is rich (REC.RICH), factories are
	--     asked for more constructors, the way a player queues a batch of
	--     builders to go clean up after a battle.
	-- Wrecks and map features carry ENERGY as well as metal, and both count.
	-- A cell's worth is its metal plus its energy at REC.E_WORTH (tripled
	-- while the team is stalling on energy); a resource whose bank is nearly
	-- full counts for nothing, so a team with full metal still goes out for
	-- energy and the other way round. Reclaim only stops when both are full.
	local REC = {
		CELL        = 512,    -- grid cell size (elmos)
		SCAN        = 300,    -- frames between field scans (~10s)
		E_WORTH     = 0.2,    -- what one unit of energy is worth next to one of metal
		E_STALL_MULT = 3,     -- ...multiplied by this while the team is stalling on energy
		MIN_FEATURE = 5,      -- ignore features worth less than this (metal + energy x E_WORTH)
		MIN_CELL    = 150,    -- a cell needs this much worth to be worth a trip
		RANGE       = 4500,   -- how far a builder will go for a cell (elmos)
		RADIUS      = 420,    -- area-reclaim radius ordered at the cell's center
		MAX         = 4,      -- most builders on reclaim at once
		PER_BUILDER = 800,    -- one crew slot per this much worth within reach of home
		RICH        = 4000,   -- worth within reach of home that makes factories add builders
		CLAIM       = 900,    -- frames a cell stays reserved for the builder sent to it (~30s)
		AVOID       = 900,    -- frames a cell is avoided after enemies were seen at it or on the way
		FULL        = 0.80,   -- a resource whose bank is fuller than this counts for nothing
		lastScan    = -99999,
		cells       = {},     -- [index] = { m = metal, e = energy, x =, z = } (worth-weighted center)
		nCellsX     = math.max(1, math.ceil(mapsizeX / 512)),
		claim       = {},     -- [teamID] = { [index] = frame the reservation expires }
		avoid       = {},     -- [teamID] = { [index] = frame the cell may be tried again }
		near        = ctx.reclaim and ctx.reclaim.near or {},   -- [teamID] = worth within reach of home
		slots       = {},     -- [teamID] = crew size the field currently supports
		reclaimable = {},     -- [featureDefID] = true/false (cached)
	}

	local function ReclaimScan(now)
		REC.lastScan = now
		local cells = REC.cells
		for idx, cell in pairs(cells) do cell.m, cell.e, cell.w, cell.x, cell.z = 0, 0, 0, 0, 0 end
		local features = Spring.GetAllFeatures()
		for i = 1, #features do
			local fid   = features[i]
			local fDefID = Spring.GetFeatureDefID(fid)
			local ok = REC.reclaimable[fDefID]
			if ok == nil then
				local fDef = FeatureDefs[fDefID]
				ok = (fDef and fDef.reclaimable and not fDef.geoThermal) and true or false
				REC.reclaimable[fDefID] = ok
			end
			if ok then
				-- returns remainingMetal, maxMetal, remainingEnergy, ...
				local metal, _, energy = Spring.GetFeatureResources(fid)
				metal, energy = metal or 0, energy or 0
				local worth = metal + energy * REC.E_WORTH
				if worth >= REC.MIN_FEATURE then
					local x, _, z = Spring.GetFeaturePosition(fid)
					if x then
						local idx  = math.floor(x / REC.CELL) + math.floor(z / REC.CELL) * REC.nCellsX
						local cell = cells[idx]
						if not cell then cell = { m = 0, e = 0, w = 0, x = 0, z = 0 }; cells[idx] = cell end
						cell.m = cell.m + metal
						cell.e = cell.e + energy
						cell.w = cell.w + worth
						cell.x = cell.x + x * worth
						cell.z = cell.z + z * worth
					end
				end
			end
		end
		for idx, cell in pairs(cells) do
			if cell.w > 0 then cell.x, cell.z = cell.x / cell.w, cell.z / cell.w end
		end
	end

	-- Per team, once per scan: how much metal lies within reach of home, and
	-- how many builders that is worth.
	local function ReclaimTeamUpdate(teamID, constructorCount)
		local home = STOR.HomeOf(teamID)
		if not home then REC.near[teamID], REC.slots[teamID] = 0, 0; return end
		local range2, total = REC.RANGE * REC.RANGE, 0
		for idx, cell in pairs(REC.cells) do
			if cell.w >= REC.MIN_CELL then
				local dx, dz = cell.x - home.x, cell.z - home.z
				if dx * dx + dz * dz <= range2 then total = total + cell.w end
			end
		end
		REC.near[teamID] = total
		local slots = math.floor(total / REC.PER_BUILDER)
		if slots < 1 and total >= REC.MIN_CELL then slots = 1 end
		local half = math.max(1, math.floor((constructorCount or 0) / 2))
		if slots > half then slots = half end
		if slots > REC.MAX then slots = REC.MAX end
		REC.slots[teamID] = slots
	end

	-- Send `unitID` to area-reclaim the best cell in its reach. wMetal and
	-- wEnergy say what each resource is worth to the team right now (0 = its
	-- bank is full). Returns true if an order went out.
	local function ReclaimOrder(unitID, teamID, now, wMetal, wEnergy)
		local ux, _, uz = Spring.GetUnitPosition(unitID)
		if not ux then return false end
		local claim = REC.claim[teamID]
		if not claim then claim = {}; REC.claim[teamID] = claim end
		local avoid = REC.avoid[teamID]
		if not avoid then avoid = {}; REC.avoid[teamID] = avoid end
		local range2 = REC.RANGE * REC.RANGE

		for attempt = 1, 3 do
			local bestIdx, bestScore, bestCell = nil, 0, nil
			for idx, cell in pairs(REC.cells) do
				local worth = cell.m * wMetal + cell.e * wEnergy
				if worth >= REC.MIN_CELL and now >= (claim[idx] or 0) and now >= (avoid[idx] or 0) then
					local dx, dz = cell.x - ux, cell.z - uz
					local d2 = dx * dx + dz * dz
					if d2 <= range2 then
						local score = worth / (math.sqrt(d2) + 600)
						-- ties broken by index so the pick does not depend on
						-- table iteration order
						if score > bestScore or (score == bestScore and bestIdx and idx < bestIdx) then
							bestIdx, bestScore, bestCell = idx, score, cell
						end
					end
				end
			end
			if not bestIdx then return false end

			-- Not under enemy guns: armed enemies at the cell or along the walk
			-- to it rule it out for a while and the next-best cell is tried.
			local hostile = Hostile(teamID, ux, uz, bestCell.x, bestCell.z)
			if hostile then
				avoid[bestIdx] = now + REC.AVOID
			elseif lib.Reachable and not lib.Reachable(teamID, Spring.GetUnitDefID(unitID), bestCell.x, bestCell.z) then
				-- wreckage the builder cannot walk to (a mesa top, across a
				-- chasm): leave it alone for a long while
				avoid[bestIdx] = now + REC.AVOID * 20
			else
				local y = Spring.GetGroundHeight(bestCell.x, bestCell.z)
				Spring.GiveOrderToUnit(unitID, CMD.RECLAIM, { bestCell.x, y, bestCell.z, REC.RADIUS }, 0)
				claim[bestIdx] = now + REC.CLAIM
				return true
			end
		end
		return false
	end
	STOR.Reclaim = ReclaimOrder
	STOR.REC     = REC

	for defID, ud in pairs(UnitDefs) do
		if ud.isBuilding and not IsFactory[defID] and not IsExtractor[defID]
				and not (ctx.IsConverter and ctx.IsConverter[defID]) and EnergyOutput(ud) <= 0
				and #(ud.weapons or {}) == 0 and not ud.canKamikaze then
			local m, e = ud.metalStorage or 0, ud.energyStorage or 0
			if m > 0 or e > 0 then
				STOR.cap[defID]  = math.max(m, e)
				STOR.capM[defID], STOR.capE[defID] = m, e
				STOR.cost[defID] = ud.metalCost or 0
			else
				local n = ud.name or ""
				if not (n:find("dragonsteeth", 1, true) or n:find("fortificationwall", 1, true)) then
					STOR.support[defID] = true   -- radar, sonar, targeting facility, air repair pad...
				end
			end
		end
	end
	do  -- one line at load: which storage defs the AI found, and their size
		local parts = {}
		for defID, cap in pairs(STOR.cap) do
			parts[#parts + 1] = UnitDefs[defID].name .. "=" .. STOR.capM[defID] .. "/" .. STOR.capE[defID] .. (STOR.geo[defID] and "(vent)" or "")
		end
		table.sort(parts)
		Spring.Echo("[SimpleAI] storage defs: " .. (#parts > 0 and table.concat(parts, ", ") or "NONE FOUND"))
	end

	-- Does the team have (or build) a tier 2+ factory? Checked per selection; the
	-- team's unit list is short enough.
	local function HasTier2Factory(teamID, units)
		for i = 1, #units do
			local d = Spring.GetUnitDefID(units[i])
			if d and IsFactory[d] and (TierOf[d] or 1) >= 2 then return true end
		end
		return false
	end

	-- TA:Recoil additions, in one table: the project selector below is at Lua
	-- 5.1's limit of 60 upvalues per function (SF kept STOR for the same reason).
	local TA = {
		AFFORD_SECS = AFFORD_SECS, AFFORD_FAC_SECS = AFFORD_FAC_SECS,
		REPAIR_BELOW = REPAIR_BELOW, REPAIR_R = REPAIR_R, ASSIST_R = ASSIST_R,
		MEX_UPGRADE_RANGE = MEX_UPGRADE_RANGE,
		CONVERTER_BASE = CONVERTER_BASE, CONVERTER_PER_E = CONVERTER_PER_E, CONVERTER_MAX = CONVERTER_MAX,
		IsAirFactory = IsAirFactory, IsSeaFactory = IsSeaFactory, IsExtractor = IsExtractor, TierOf = TierOf,
		FindMexSpot = FindMexSpot, FindMexUpgrade = FindMexUpgrade, EnergyOutput = EnergyOutput,
		LAND_FAC_MIN = LAND_FAC_MIN, MEX_TARGET_EARLY = MEX_TARGET_EARLY, MEX_TARGET_MID = MEX_TARGET_MID,
		MEX_RANGE_EARLY = MEX_RANGE_EARLY, MEX_RANGE_MID = MEX_RANGE_MID,
		HasTier2Factory = HasTier2Factory,
	}

	local B = { name = "construction", order = 40 }

	function B.TeamInit(teamID)
		STOR.lastStart[teamID] = -STOR.SPACING
		JOB.of[teamID]     = {}
		JOB.active[teamID] = { gen = 0, tur = 0, rec = 0, genOut = 0 }
		SimpleFactoryDelay[teamID]     = 0
		SimpleConstructorDelay[teamID] = 0
		-- Negative seeds so the very first constructor/factory are not gated
		-- by the spacing limiters at game start.
		SimpleLastConStart[teamID]     = -CON_BUILD_SPACING
		SimpleLastFacStart[teamID]     = -FACTORY_SPACING
	end

	--------------------------------------------------------------------------
	-- CONSTRUCTION PROJECT SELECTION
	-- The shared "build something sensible" engine, used by constructors and
	-- factories here and by the commander via the services registry.
	--------------------------------------------------------------------------
	local function SimpleConstructionProjectSelection(
			unitID, unitDefID, unitTeam, allyTeamID, units, allunits, buildType)

		local success = false
		local rung    = "F"   -- which priority rung took this unit (decision trace)

		local nowFrame   = Spring.GetGameFrame()
		-- Adaptive difficulty pacing: >1 slows every constructor/factory start
		-- window, <1 tightens them. Resolved via the services registry because
		-- this selector is also called from b_commander without a tick in hand.
		-- nil (plain SimpleAI teams, or b_adaptive absent) -> stock 1.0.
		local knobsK     = services.GetKnobs and services.GetKnobs(unitTeam)
		local pacingMult = knobsK and knobsK.pacingMult or 1
		-- True only if enough frames have passed since this team last STARTED a
		-- constructor. Shared by every factory/builder so the whole team starts at
		-- most one constructor per CON_BUILD_SPACING, letting the count catch up.
		local conSpacingOk = (nowFrame - (SimpleLastConStart[unitTeam] or 0))
				>= CON_BUILD_SPACING * pacingMult

		-- Unit limit (the game's MaxUnits): the only cap on numbers in TA.
		local maxUnits, curUnits = Spring.GetTeamMaxUnits(unitTeam)
		local unitRoom = (maxUnits or 1000) - (curUnits or 0)
		local mcurrent, mstorage, _, mincome = Spring.GetTeamResources(unitTeam, "metal")
		local ecurrent, estorage, epull, eincome = Spring.GetTeamResources(unitTeam, "energy")
		-- Signal pools: the denominators for every stock-ratio threshold
		-- below. Equal to raw storage until storage has been built.
		local mpool = SignalPool(mstorage, mincome)
		local epool = SignalPool(estorage, eincome)
		local unitposx, unitposy, unitposz   = Spring.GetUnitPosition(unitID)
		local buildOptions = UnitDefs[unitDefID].buildOptions
		local techLevel    = TeamTechLevel[unitTeam] or 1

		-- Factory pacing: a single per-team frame limiter (no escalating delay), so
		-- factory #8 starts as readily as factory #2. When both metal and energy are
		-- piling up we drop to the faster "flood" spacing and pour the surplus into
		-- new production lines.
		local overflowing  = mstorage > 0 and estorage > 0
				and mcurrent > mpool * FACTORY_OVERFLOW
				and ecurrent > epool * FACTORY_OVERFLOW
		local facSpacing   = (overflowing and FACTORY_SPACING_FLOOD or FACTORY_SPACING)
				* pacingMult
		local facSpacingOk = (nowFrame - (SimpleLastFacStart[unitTeam] or 0)) >= facSpacing

		-- Factory room. Factories used to be added whenever the bank looked
		-- healthy, up to twelve. A recorded team ended up with eight, six or
		-- seven of them paused for 25 minutes because its metal could feed
		-- only one or two. Two limits now apply to every factory after the
		-- first: the count is tied to metal income, and none is added while
		-- the throttle has had to pause one in the last couple of minutes
		-- (a paused factory is spare capacity already).
		if (STOR.stallPaused[unitTeam] or 0) > 0 then STOR.lastPaused[unitTeam] = nowFrame end
		local facAllowed = math.min(FACTORY_MAX, STOR.FAC_BASE + math.floor(mincome / STOR.FAC_INCOME_EACH))
		local facRoom = SimpleFactoriesCount[unitTeam] < facAllowed
				and (nowFrame - (STOR.lastPaused[unitTeam] or -99999)) >= STOR.FAC_PAUSE_MEMORY

		-- econPressure: 0 = at target, approaches 1 when far below next tech threshold
		local goal = TECH_INCOME_GOALS[techLevel]
		local econPressure = 0
		if goal and techLevel < 4 then
			local mRatio = (goal.m > 0) and math.min(1, mincome / goal.m) or 1
			local eRatio = (goal.e > 0) and math.min(1, eincome / goal.e) or 1
			econPressure = TECH_ECONOMY_BIAS * (1 - math.min(mRatio, eRatio))
		end

		-- Stall signal (owned by the core): how far demand outruns income,
		-- 0..1. `stalling` (combined, metal discounted) gates adding
		-- factories and keeps factory queues short. `eStalling` (energy
		-- only) is what makes factories lean toward cheap units and stops
		-- new constructors: energy cost climbs with tech, so that is the
		-- stall cheaper production can actually fix.
		local eStall    = STOR.stallE[unitTeam] or 0
		local stalling  = (STOR.stallV[unitTeam] or 0) >= STOR.STALL_ON
		local eStalling = eStall >= STOR.STALL_ON

		local function CanMake(defID)
			for i2 = 1, #buildOptions do
				if buildOptions[i2] == defID then return true end
			end
			return false
		end

		-- TryBuild: a random pick among the defs in defList that this builder
		-- can make AND can pay for: metal cost at most the bank plus `secs`
		-- seconds of income (TA.AFFORD_SECS unless given). If nothing fits the
		-- budget, the cheapest it can make. (SF picked any def it could make:
		-- in TA that was a Guardian or an Advanced lab at minute three.)
		local function TryBuild(defList, orderFn, secs)
			if not defList or #defList == 0 then return false end
			local budget = mcurrent + mincome * (secs or TA.AFFORD_SECS)
			local cands, cheapest, cheapestCost = {}, nil, math.huge
			for _, project in ipairs(defList) do
				if CanMake(project) then
					local cost = UnitDefs[project].metalCost or 0
					if cost <= budget then cands[#cands + 1] = project end
					if cost < cheapestCost then cheapest, cheapestCost = project, cost end
				end
			end
			if #cands == 0 then
				if not cheapest then return false end
				cands[1] = cheapest
			end
			orderFn(cands[math.random(1, #cands)])
			return true
		end

		-- Weighted-random variant: takes {id=,w=} pairs (from GetWeightedBuildable),
		-- filters to what this builder/factory can actually make, and picks one with
		-- probability proportional to weight. Used for combat composition control.
		local function TryBuildWeighted(weighted, orderFn)
			if not weighted or #weighted == 0 then return false end
			local cands, total = {}, 0
			for _, e in ipairs(weighted) do
				for i2 = 1, #buildOptions do
					if buildOptions[i2] == e.id then
						cands[#cands + 1] = e
						total = total + e.w
						break
					end
				end
			end
			if total <= 0 then return false end
			-- While stalling on ENERGY, lean toward units that are cheap in
			-- energy: weight x (cheapest / cost) ^ (POWER x stall). At the
			-- stall threshold that is roughly "ten times the price, a sixth
			-- as likely"; a deep stall all but rules expensive units out.
			-- Energy cost climbs with tech level in SF, so this steers
			-- production back toward lower tiers until income catches up.
			local wOf = nil
			if eStalling then
				local minCost = math.huge
				for _, e in ipairs(cands) do
					local cost = UnitDefs[e.id].energyCost or 0
					if cost < 1 then cost = 1 end
					if cost < minCost then minCost = cost end
				end
				local power = STOR.STALL_COST_POWER * eStall
				wOf, total = {}, 0
				for i2, e in ipairs(cands) do
					local cost = UnitDefs[e.id].energyCost or 0
					if cost < 1 then cost = 1 end
					wOf[i2] = e.w * (minCost / cost) ^ power
					total = total + wOf[i2]
				end
				if total <= 0 then return false end
			end
			local roll, acc = math.random() * total, 0
			for i2, e in ipairs(cands) do
				acc = acc + (wOf and wOf[i2] or e.w)
				if roll <= acc then
					orderFn(e.id)
					return true
				end
			end
			orderFn(cands[#cands].id)   -- float-rounding fallback
			return true
		end

		local function NearMe(project)
			local x, y, z = Spring.GetUnitPosition(unitID)
			-- Use a larger offset so we don't place inside the caller's own footprint.
			-- Also nudge away from map edges.
			local ox = math.random(-256, 256)
			local oz = math.random(-256, 256)
			if x + ox < 256 then ox = math.abs(ox) end
			if x + ox > mapsizeX - 256 then ox = -math.abs(ox) end
			if z + oz < 256 then oz = math.abs(oz) end
			if z + oz > mapsizeZ - 256 then oz = -math.abs(oz) end
			local bx, bz = x + ox, z + oz
			local by = Spring.GetGroundHeight(bx, bz)
			local facing = math.random(0, 3)
			local testpos = Spring.TestBuildOrder(project, bx, by, bz, facing)
			if testpos == 2 then
				Spring.GiveOrderToUnit(unitID, -project, { bx, by, bz, facing }, 0)
			else
				-- Fall back to SimpleBuildOrder if direct placement failed
				SimpleBuildOrder(unitID, project)
			end
		end

		local function AtMex(project, spot)
			Spring.GiveOrderToUnit(unitID, -project,
			                       { spot.x, spot.y, spot.z, 0 }, { "shift" })
		end

		SimpleFactoryDelay[unitTeam]     = SimpleFactoryDelay[unitTeam] - 1
		SimpleConstructorDelay[unitTeam] = SimpleConstructorDelay[unitTeam] - 1

		local r = math.random(0, 20)

		-- Water: buildings that need water (minWaterDepth > 0: shipyards,
		-- tidal, floating and underwater things) are only offered when the
		-- team's home has water nearby (lib.WaterNear).
		local wet = lib.WaterNear and lib.WaterNear(unitTeam) or false
		local function LandOK(list)
			if wet then return list end
			local out = {}
			for _, id in ipairs(list) do
				if (UnitDefs[id].minWaterDepth or 0) <= 0 then out[#out + 1] = id end
			end
			return out
		end

		-- Fetch current tech-appropriate lists, cut down to what THIS builder
		-- can make. (SF's lists were per faction and tech and every builder
		-- could make most of them; a TA T1 constructor cannot make a T2 AA
		-- tower, and a rung that picked one failed and ate the builder's turn
		-- every tick.) A rung whose list is empty is skipped instead.
		local function Mine(list)
			local out = {}
			for _, id in ipairs(list) do
				if CanMake(id) then out[#out + 1] = id end
			end
			return out
		end
		local extractors   = Mine(GetBuildable(unitTeam, "extractor"))   -- (the spot decides land / water)
		local generators   = Mine(LandOK(GetBuildable(unitTeam, "generator")))
		local converters   = Mine(LandOK(GetBuildable(unitTeam, "converter")))
		local turrets      = Mine(LandOK(GetBuildable(unitTeam, "turret")))
		local storages     = Mine(LandOK(GetBuildable(unitTeam, "storage")))
		local factories    = Mine(GetBuildableTechBiased(unitTeam, "factory", TECH_FAC_BIAS))
		local constructors = Mine(GetBuildable(unitTeam, "constructor"))
		local combats      = GetWeightedBuildable(unitTeam, "combat", TECH_UNIT_BIAS, CombatRoleWeight)
		local buildings    = Mine(LandOK(GetBuildable(unitTeam, "building")))
		-- air repair pads only make sense with an air force
		if (ctx.counters.airFactories[unitTeam] or 0) == 0 then
			local out = {}
			for _, id in ipairs(buildings) do
				if not UnitDefs[id].isAirBase then out[#out + 1] = id end
			end
			buildings = out
		end

		-- Dynamic mex search range: cast a wide net once we have factories running
		local mexRange  = (SimpleFactoriesCount[unitTeam] >= 1) and TA.MEX_RANGE_MID or TA.MEX_RANGE_EARLY
		local myDefID   = Spring.GetUnitDefID(unitID)
		local commLeash = (buildType == "Commander") and STOR.BASE.CommLeash(unitTeam, unitID) or nil
		local commHome  = commLeash and STOR.HomeOf(unitTeam)
		-- A spot comes with the extractor that fits it (land mex or underwater
		-- mex, the cheapest this builder can make there). Basic extractors
		-- only: mohos go on top of mexes (rung MOHO), not on bare spots.
		local basicMex = {}
		for _, id in ipairs(extractors) do
			if (TA.TierOf[id] or 1) == 1 then basicMex[#basicMex + 1] = id end
		end
		local mexspot, mexDef
		if commHome then
			-- the commander only takes metal spots inside its leash of home
			mexspot, mexDef = TA.FindMexSpot(commHome.x, commHome.z, commLeash, unitTeam, myDefID, basicMex, CanMake)
		else
			mexspot, mexDef = TA.FindMexSpot(unitposx, unitposz, mexRange, unitTeam, myDefID, basicMex, CanMake)
		end
		-- Also look globally for any unclaimed mex (no range limit) for roaming decisions
		local mexAny, mexAnyDef
		if not commHome and buildType ~= "Factory" then
			if mexspot then
				mexAny, mexAnyDef = mexspot, mexDef
			else
				mexAny, mexAnyDef = TA.FindMexSpot(unitposx, unitposz, nil, unitTeam, myDefID, basicMex, CanMake)
			end
		end

		-- Split factories: only offer air/sea once we have enough land
		-- factories; sea factories only near water.
		local landFacCount  = SimpleLandFacCount[unitTeam] or 0
		local landFactories = {}
		local allFactories = {}
		for _, id in ipairs(factories) do
			if TA.IsSeaFactory[id] then
				if wet then allFactories[#allFactories + 1] = id end
			elseif TA.IsAirFactory[id] then
				allFactories[#allFactories + 1] = id
			else
				landFactories[#landFactories + 1] = id
				allFactories[#allFactories + 1] = id
			end
		end
		-- Before TA.LAND_FAC_MIN land factories, only offer land factories
		if landFacCount < TA.LAND_FAC_MIN then
			factories = landFactories
		else
			factories = allFactories
		end
		-- Teching up: with two factories standing and no advanced one yet, the
		-- next factory this builder starts is an advanced lab if it can make
		-- one (TA's T1 labs are slow and cheap; the game is won at T2).
		if SimpleFactoriesCount[unitTeam] >= 2 and not TA.HasTier2Factory(unitTeam, units) then
			local adv = {}
			for _, id in ipairs(factories) do
				if (TA.TierOf[id] or 1) >= 2 then adv[#adv + 1] = id end
			end
			if #adv > 0 then factories = adv end
		end

		-- Dedicated AA subset of the buildable turret list. Small list,
		-- filtered per call; the generic turret bucket keeps its AA entries
		-- too, so the random baseline mix is unchanged.
		local aaTurrets = {}
		for _, id in ipairs(turrets) do
			if IsAATurret[id] then aaTurrets[#aaTurrets + 1] = id end
		end

		local turretCount  = SimpleTurretCount[unitTeam] or 0
		local belowTurretCap = turretCount < TURRET_CAP
		-- How many turrets this base actually wants, scaled to its size.
		local desiredTurrets = math.min(TURRET_CAP,
			TURRET_BASE
			+ (SimpleFactoriesCount[unitTeam] or 0) * TURRET_PER_FAC
			+ math.floor((SimpleT1Mexes[unitTeam] or 0) / TURRET_PER_MEX_DIV))
		local underDefended = (SimpleFactoriesCount[unitTeam] or 0) > 0
			and turretCount < desiredTurrets and belowTurretCap
		local canAffordTurret = ecurrent > epool * 0.20 and mcurrent > mpool * 0.15

		-- AA demand: only while air evidence is fresh, only if this faction
		-- actually has AA turrets buildable at current tech, only below the
		-- AA and overall turret caps.
		local airStamp  = SimpleAirThreat[unitTeam]
		local airFresh  = airStamp and (nowFrame - airStamp) < AA_THREAT_MEMORY
		local desiredAA = math.min(AA_CAP, AA_BASE
			+ math.floor((SimpleFactoriesCount[unitTeam] or 0) / AA_PER_FAC_DIV))
		local needAA    = airFresh and #aaTurrets > 0
			and (SimpleAATurretCount[unitTeam] or 0) < desiredAA
			and belowTurretCap and canAffordTurret

		-- Herd control (see JOB). This unit is idle, so whatever it was doing
		-- for a capped need is over.
		local jobs, active = JOB.of[unitTeam], JOB.active[unitTeam]
		if jobs and jobs[unitID] then
			active[jobs[unitID]] = math.max(0, active[jobs[unitID]] - 1)
			jobs[unitID] = nil
		end
		local genRoom = (not active) or active.gen < JOB.MAX.gen
		-- Base work is for builders near home (see BASE). A builder out in the
		-- field takes field work; with none left it walks home (rung "home").
		local nearHome = true
		if buildType == "Builder" then
			local home = STOR.HomeOf(unitTeam)
			if home then
				local hdx, hdz = unitposx - home.x, unitposz - home.z
				nearHome = (hdx * hdx + hdz * hdz) <= STOR.BASE.RANGE * STOR.BASE.RANGE
			end
		end
		local turretRoom = (not active) or active.tur < JOB.MAX.tur
		if not turretRoom then
			underDefended, needAA = false, false
		end
		-- Reclaim (see REC). What each resource is worth to the team right
		-- now: nothing if its bank is nearly full, and energy counts triple
		-- while the team is stalling on it. Both zero = nothing to gain.
		local recWM = (mcurrent < mstorage * STOR.REC.FULL) and 1 or 0
		local recWE = (ecurrent < estorage * STOR.REC.FULL)
				and STOR.REC.E_WORTH * (eStalling and STOR.REC.E_STALL_MULT or 1) or 0
		local reclaimUseful = (recWM + recWE) > 0
		-- Reclaim crew: builders only, while the field supports another crew
		-- member.
		local reclaimOk = buildType == "Builder" and active and reclaimUseful
				and active.rec < (STOR.REC.slots[unitTeam] or 0)
				and SimpleFactoriesCount[unitTeam] > 0

		-- Forward defense (see FWD): builders only, one start per spacing
		-- window, never while stalling, and only with room under the turret
		-- cap. Whether a forward site actually needs a turret is decided
		-- inside the rung, by STOR.Forward.
		local forwardOk = buildType == "Builder" and turretRoom and belowTurretCap
				and not stalling
				and SimpleFactoriesCount[unitTeam] > 0
				and (nowFrame - (STOR.FWD.last[unitTeam] or -99999)) >= STOR.FWD.SPACING * pacingMult
		-- The energy rung's own trigger, unchanged; genRoom decides whether
		-- THIS builder may answer it.
		-- (TA scale: a solar is 20 E/s. Before the first factory a commander and
		-- two solars are enough; the econ pressure and stall rungs take over later.)
		-- Energy is what limits a TA economy (every unit costs several times
		-- its metal in energy): wanted whenever demand (pull) outruns income,
		-- the bank is under half, or the floor is not met. URGENT (rung P2
		-- before everything but the opening mexes) when the bank is low or
		-- the team is stalling on it.
		local energyWanted = ecurrent < epool * 0.50
				or eincome < (epull or 0) * 1.15
				or eincome <= (SimpleFactoriesCount[unitTeam] == 0 and 40 or 80)
				or (econPressure > 0.5 and goal and eincome < goal.e * 0.6)
				or eStalling   -- demand is outrunning income, whatever the bank says

		-- Repair, assist, moho, strategic (TA additions; see the rungs REP,
		-- AS, FB.assist, MOHO, ST). Builders only, and only near home or in
		-- the field they are already in; the commander repairs within its
		-- leash and assists nothing (it has better things to do).
		local isBuilder = (buildType == "Builder")
		local repairOk  = (isBuilder or buildType == "Commander") and active and active.rep < JOB.MAX.rep
		local assistOk  = (isBuilder or buildType == "Commander") and active and active.as < JOB.MAX.as
		local hurt, nanoframe, factoryToAssist
		if repairOk or assistOk then
			local reach = (buildType == "Commander") and math.min(TA.REPAIR_R, commLeash or TA.REPAIR_R) or TA.REPAIR_R
			local near = Spring.GetUnitsInCylinder(unitposx, unitposz, reach, unitTeam)
			local hurtBest, nanoBest, facBest = 0, nil, -1
			for i2 = 1, #near do
				local other = near[i2]
				if other ~= unitID then
					local oDef = Spring.GetUnitDefID(other)
					local h, mh, _, _, bp = Spring.GetUnitHealth(other)
					if oDef and h and mh and mh > 0 then
						local ox, _, oz = Spring.GetUnitPosition(other)
						local d2 = (ox - unitposx) ^ 2 + (oz - unitposz) ^ 2
						if (bp or 1) < 1 then
							-- a nanoframe: ours, not being built by anyone, within
							-- assist reach (a factory's own pad is not a nanoframe
							-- we should walk into: skip units being built BY a factory)
							if assistOk and d2 <= TA.ASSIST_R * TA.ASSIST_R and UnitDefs[oDef].isBuilding
									and not Spring.GetUnitIsBeingBuilt(other) == false then
								local builders = Spring.GetUnitsInCylinder(ox, oz, 250, unitTeam)
								local working = false
								for b2 = 1, #builders do
									if builders[b2] ~= unitID and Spring.GetUnitIsBuilding(builders[b2]) == other then working = true; break end
								end
								if not working and (not nanoBest or d2 < nanoBest) then nanoframe, nanoBest = other, d2 end
							end
						elseif repairOk and h / mh < TA.REPAIR_BELOW and not (IsFactory[oDef] and false) then
							-- hurt and not under fire right now (nothing armed and hostile close to it)
							local score = (1 - h / mh) * mh / (1 + math.sqrt(d2) / 400)
							if score > hurtBest then
								local foe = Spring.GetUnitNearestEnemy(other, 500, true)
								if not foe then hurt, hurtBest = other, score end
							end
						elseif assistOk and IsFactory[oDef] and d2 <= TA.ASSIST_R * TA.ASSIST_R then
							local q = #(Spring.GetFullBuildQueue(other, 0) or {})
							if q > facBest then factoryToAssist, facBest = other, q end
						end
					end
				end
			end
			if facBest < 1 then factoryToAssist = nil end   -- an idle factory needs no help
		end
		-- Moho on mex: the nearest basic mex of ours that an advanced
		-- extractor this builder can make fits on.
		local mohoDef, mohoX, mohoY, mohoZ
		if isBuilder and (TeamTechLevel[unitTeam] or 1) >= 2 and SimpleFactoriesCount[unitTeam] > 0 then
			local mexUnit
			mexUnit, mohoX, mohoY, mohoZ, mohoDef = TA.FindMexUpgrade(unitposx, unitposz, TA.MEX_UPGRADE_RANGE, unitTeam, myDefID,
				extractors, CanMake, TA.IsExtractor, TA.TierOf)
			if not mexUnit then mohoDef = nil end
		end
		-- Strategic: a silo or anti-nuke the strategic behavior wants built.
		local stratWant = (isBuilder and services.StrategicWant) and services.StrategicWant(unitTeam, nowFrame) or nil

		-- Power plant sizing. The energy rungs used to pick any plant the
		-- builder could make, favoring the highest tier. A recorded team
		-- answered a shortfall of a few thousand E/s with two black hole
		-- plants (40,000 E/s) and threw away 63% of its energy for half the
		-- game. Now the plant is chosen to fit the need:
		--   need = what the team is trying to spend beyond what it earns,
		--          with some headroom; at least the gap to the next tech
		--          goal; at least a modest growth step;
		--          MINUS the output of plants builders are already on.
		--   pick = the biggest affordable plant that does not overshoot the
		--          need by more than half; if even the smallest would, the
		--          smallest. (The first version took "the smallest plant
		--          that covers the need", and the tiers are so far apart,
		--          2,700 then 20,000, that any need above 2,700 bought a
		--          black hole. It also trusted the engine's "pull" figure,
		--          which during a stall is everything the team WISHES it
		--          could spend; the shortfall is now capped at twice the
		--          current income, so capacity grows in steps.)
		-- No need left once pending plants are counted = no plant (nil).
		local function GeneratorPick()
			local short = (epull or 0) - eincome
			if short < 0 then short = 0 end
			local step = eincome * STOR.GEN_MAX_STEP + STOR.GEN_STEP_FLOOR
			if short > step then short = step end
			local need = short * STOR.GEN_HEADROOM
			if goal and eincome < goal.e then need = math.max(need, goal.e - eincome) end
			need = math.max(need, eincome * STOR.GEN_GROWTH, STOR.GEN_MIN)
			need = need - ((active and active.genOut) or 0)
			if need <= 0 then return nil end
			local budget  = mincome * STOR.GEN_COST_SECS + mcurrent
			local ceiling = need * STOR.GEN_OVERSHOOT
			local fit, fitOut, smallest, smallestOut, cheapest, cheapestCost, anyMake
			for _, id in ipairs(generators) do
				if CanMake(id) and (not STOR.geo[id] or STOR.GeoSpotFor(unitID, id)) then
					local ud   = UnitDefs[id]
					local out  = TA.EnergyOutput(ud)
					local cost = ud.metalCost or 0
					anyMake = anyMake or id
					if out > 0 then
						if not cheapest or cost < cheapestCost then cheapest, cheapestCost = id, cost end
						if cost <= budget then
							if out <= ceiling and (not fit or out > fitOut) then fit, fitOut = id, out end
							if not smallest or out < smallestOut then smallest, smallestOut = id, out end
						end
					end
				end
			end
			-- (anyMake: plants that do not declare an output, e.g. wind or
			-- tidal style generators, are still buildable as a last resort)
			return fit or smallest or cheapest or anyMake
		end
		local genPick = (genRoom and nearHome) and GeneratorPick() or nil
		-- TA's T1 plants are small (solar 20 E): order up to GEN_BATCH of them in
		-- one go (queued with shift) so one builder's trip raises income by a
		-- useful step. Big plants go one at a time.
		local GEN_BATCH = 3
		local function OrderPower(defID)
			local out = TA.EnergyOutput(UnitDefs[defID])
			local n = 1
			if out > 0 and out < 50 then n = math.min(GEN_BATCH, math.max(1, math.ceil(60 / out))) end
			local ok = false
			for i = 1, n do
				if SimpleBuildOrder(unitID, defID) then ok = true else break end
			end
			return ok
		end
		local energyUrgent = genPick ~= nil and (ecurrent < epool * 0.35 or eStalling)

		-- Metal makers (TA's energy -> metal sink): wanted when energy brims
		-- and metal is the short resource, up to a count that grows with
		-- energy income. Never while stalling on energy.
		local converterCap = math.min(TA.CONVERTER_MAX, TA.CONVERTER_BASE + math.floor(eincome / TA.CONVERTER_PER_E))
		local wantConverter = #converters > 0 and not eStalling
				and SimpleFactoriesCount[unitTeam] > 0
				and (SimpleConverterCount[unitTeam] or 0) < converterCap
				and ecurrent > epool * 0.70 and eincome >= 120
				and mcurrent < mpool * 0.50
		-- energy plainly floating while metal is short: makers before anything but the opening
		local energyFloating = wantConverter and ecurrent > epool * 0.90 and mcurrent < mpool * 0.30

		-- Storage demand, per resource (TA storages hold one or the other).
		-- `storagePick` is the def this builder should raise right now, or
		-- nil. Capacity that is ordered but not yet finished blocks further
		-- starts (STOR.pending), so four idle builders in the same tick
		-- cannot all start one.
		local storagePick
		local haveStorage, wantStorage = 0, 0
		do
			local function Want(res, have, income, current)
				local ceil  = (STOR.TECH_CEIL[res][techLevel] or STOR.GOAL)
				local want  = income * (res == "m" and STOR.INCOME_SECS_M or STOR.INCOME_SECS_E)
				if current > have * STOR.BRIM and income > 0 then want = ceil end   -- brimming: take the next step now
				if want > ceil then want = ceil end
				local floor = STOR.TECH_FLOOR[res][techLevel] or 0
				if want < floor then want = floor end
				return want
			end
			local wantM, wantE = Want("m", mstorage, mincome, mcurrent), Want("e", estorage, eincome, ecurrent)
			local gapM, gapE = wantM - mstorage, wantE - estorage
			-- the resource that is furthest behind its schedule goes first
			local res, gap, capOf
			if gapE / math.max(1, wantE) >= gapM / math.max(1, wantM) then
				res, gap, capOf, haveStorage, wantStorage = "e", gapE, STOR.capE, estorage, wantE
			else
				res, gap, capOf, haveStorage, wantStorage = "m", gapM, STOR.capM, mstorage, wantM
			end

			local pendingAt = STOR.pending[unitTeam]
			if pendingAt and (nowFrame - pendingAt) >= STOR.PENDING_MAX then
				STOR.pending[unitTeam] = nil   -- builder died or order was lost
				pendingAt = nil
			end

			-- No "can we afford it" gate here on purpose: a team that spends
			-- everything it earns sits at the bottom of its pool permanently
			-- (AdaptiveAI rests exactly ON the NeverStall floor), so any such
			-- gate reads "broke" forever. The one-at-a-time lock, the spacing
			-- and the income-proportional size pick are the brakes instead.
			local spacingOk = (nowFrame - (STOR.lastStart[unitTeam] or 0))
					>= STOR.SPACING * pacingMult
			if gap > 0 and not pendingAt
					and #storages > 0
					and SimpleFactoriesCount[unitTeam] > 0
					and (SimpleT1Mexes[unitTeam] or 0) >= STOR.MIN_MEXES
					and nowFrame >= (STOR.retryAt[unitTeam] or 0)
					and spacingOk then
				-- Biggest storage this builder can make that is neither out
				-- of proportion to income nor far past the gap; otherwise the
				-- smallest one that is still worth building. Sizes too small
				-- to matter for this gap are skipped, so a tech 2+ base does
				-- not get carpeted in small storages.
				local costBudget = mincome * STOR.COST_SECS
				local minCap     = gap / STOR.MAX_STEPS
				-- Vent storage (the condenser) is a candidate only when a free
				-- vent is within this builder's reach; on equal capacity the
				-- cheaper building wins, which is how the condenser beats
				-- medium storage wherever a vent is available.
				local bestCap, bestCost, smallest, smallestCap = 0, math.huge, nil, math.huge
				for _, id in ipairs(storages) do
					local cap = capOf[id] or 0
					if cap > 0 and cap >= minCap and CanMake(id)
							and (not STOR.geo[id] or STOR.GeoSpotFor(unitID, id)) then
						local cost = STOR.cost[id] or 0
						if cap < smallestCap then smallest, smallestCap = id, cap end
						if (cap > bestCap or (cap == bestCap and cost < bestCost))
								and cost <= costBudget
								and cap <= gap * STOR.FIT then
							storagePick, bestCap, bestCost = id, cap, cost
						end
					end
				end
				storagePick = storagePick or smallest
			end

			if STOR.DEBUG and gap > 0 and not storagePick and not pendingAt and spacingOk
					and buildType ~= "Factory"
					and nowFrame >= (STOR.dbgAt[unitTeam] or 0) then
				STOR.dbgAt[unitTeam] = nowFrame + 900
				Spring.Echo(("[SimpleAI] storage: team %d tech %d has %d wants %d but no pick"
					.. " (storage defs at this tech: %d, factories: %d, builder: %s)"):format(
					unitTeam, techLevel, haveStorage, wantStorage, #storages,
					SimpleFactoriesCount[unitTeam] or 0, UnitDefs[unitDefID].name))
			end
		end

		-- -------------------------------------------------------
		-- BUILDER / COMMANDER priority chain
		-- -------------------------------------------------------
		if buildType == "Builder" or buildType == "Commander" then

			-- PRIORITY 1: early mexes (always grab the first few immediately)
			if mexspot and SimpleT1Mexes[unitTeam] < TA.MEX_TARGET_EARLY then
				rung = "P1"
				AtMex(mexDef, mexspot)
				success = true

				-- PRIORITY 5: the first factory, as soon as the opening mexes are
				-- down and the bank can carry it (a TA opening: mex, mex, mex,
				-- factory, then power). Energy stalls are the energy rung's job.
			elseif SimpleFactoriesCount[unitTeam] == 0 and SimpleFactoryDelay[unitTeam] <= 0
					and (ecurrent > epool * 0.30 or mcurrent >= 600) and #factories > 0 then
				rung = "P5"
				if TryBuild(factories, function(p) SimpleBuildOrder(unitID, p) end, TA.AFFORD_FAC_SECS) then
					SimpleFactoryDelay[unitTeam] = 120
					SimpleLastFacStart[unitTeam] = nowFrame
					success = true
				end

				-- PRIORITY P2 (urgent): the energy bank is low or the team is
				-- stalling on energy. In TA nothing gets built without it.
			elseif energyUrgent then
				rung = "P2"
				success = OrderPower(genPick)

				-- PRIORITY MM (early): energy brimming, metal gone: metal makers now.
			elseif energyFloating and genRoom and nearHome then
				rung = "MM"
				if TryBuild(converters, function(p) SimpleBuildOrder(unitID, p) end) then
					SimpleConverterCount[unitTeam] = SimpleConverterCount[unitTeam] + 1
					success = true
				end

				-- PRIORITY 6a: a defence floor. TA bases get an LLT or two early;
				-- below one turret per factory this fires even before mex
				-- expansion (the reactive and steady rungs do the rest).
			elseif buildType ~= "Commander" and #turrets > 0 and canAffordTurret and turretRoom
					and turretCount < math.min(desiredTurrets, SimpleFactoriesCount[unitTeam]) then
				rung = "6b"
				success = TryBuild(turrets, function(p) SimpleBuildOrder(unitID, p) end)

				-- PRIORITY 6: mex expansion. TA maps carry dozens of spots and
				-- metal is the whole game, so this comes before power and
				-- storage (SF, with few spots, had it far down). Needs a little
				-- energy in the bank and a safe road to the spot.
			elseif mexspot and SimpleT1Mexes[unitTeam] < TA.MEX_TARGET_MID
					and SimpleFactoriesCount[unitTeam] > 0
					and ecurrent > epool * 0.25
					and not STOR.Hostile(unitTeam, unitposx, unitposz, mexspot.x, mexspot.z) then
				rung = "P6"
				AtMex(mexDef, mexspot)
				success = true

				-- PRIORITY 9: more factories, as soon as both banks are healthy (TA: a second
				-- factory beats more power; the energy rung below catches up)
				-- (TA: a factory drains the metal bank by design, so the bank is
				-- no measure of room for another; income is, via facRoom.)
			elseif not stalling and nearHome and ecurrent > epool * 0.40 and mcurrent > mpool * 0.20
					and facRoom and #factories > 0
					and eincome >= 80 + 50 * SimpleFactoriesCount[unitTeam]   -- power for one more factory
					and facSpacingOk then
				rung = "P9"
				if TryBuild(factories, function(p) SimpleBuildOrder(unitID, p) end, TA.AFFORD_FAC_SECS) then
					SimpleLastFacStart[unitTeam] = nowFrame
					success = true
				end

				-- PRIORITY 5s: STORAGE growth. The team is below its storage
				-- schedule (or brimming) and nothing is already on order.
				-- Sits ABOVE the energy rung on purpose. A recorded game showed
				-- why: once income outgrows the bank (9,000 E/s into 2,600
				-- storage) the stock reads near zero every tick, the energy
				-- rung below fires forever, and nothing under it ever runs,
				-- storage included, which is the one thing that would fix the
				-- reading. storagePick already carries the pacing (one project
				-- at a time, spaced out), so this costs one builder briefly.
			elseif storagePick and nearHome and not eStalling and ecurrent > epool * 0.5 then
				rung = "5s"
				if SimpleBuildOrder(unitID, storagePick) then
					STOR.lastStart[unitTeam] = nowFrame
					STOR.pending[unitTeam]   = nowFrame
					success = true
					if STOR.DEBUG then
						Spring.Echo(("[SimpleAI] storage: team %d tech %d ordered %s (has %d, wants %d)"):format(
							unitTeam, techLevel, UnitDefs[storagePick].name, haveStorage, wantStorage))
					end
				else
					-- (no back-off while the brick planner is mid-search: its
					-- scan resumes on the next call)
					STOR.retryAt[unitTeam] = nowFrame + ((lib.brickResult == "searching") and 0 or STOR.RETRY)
					-- Why not: tally the placement search's own reasons into
					-- the trace (5s.blocked / 5s.occupied / 5s.crowded /
					-- 5s.noanchor are candidate-site counts).
					local ps    = (not STOR.geo[storagePick]) and lib.placeStats
					local tally = STOR.trace[unitTeam]
					if ps and tally then
						tally["5s.blocked"]  = (tally["5s.blocked"]  or 0) + ps.blocked
						tally["5s.occupied"] = (tally["5s.occupied"] or 0) + ps.occupied
						tally["5s.crowded"]  = (tally["5s.crowded"]  or 0) + ps.crowded
						tally["5s.noanchor"] = (tally["5s.noanchor"] or 0) + ps.noAnchor
					end
					if STOR.DEBUG then
						Spring.Echo(("[SimpleAI] storage: team %d found no place for %s by %s"
							.. " (sites %d: blocked %d, occupied %d, crowded %d; empty rings %d)"):format(
							unitTeam, UnitDefs[storagePick].name, UnitDefs[unitDefID].name,
							ps and ps.sites or -1, ps and ps.blocked or -1, ps and ps.occupied or -1,
							ps and ps.crowded or -1, ps and ps.noAnchor or -1))
					end
					storagePick = nil   -- tried and failed; not "preempted"
				end

				-- PRIORITY 2: energy - urgent if low or econ pressure is high
			elseif energyWanted and genRoom and nearHome and genPick then
				rung = "P2"
				success = OrderPower(genPick)   -- sized to the shortfall (GeneratorPick)

				-- PRIORITY 3: metal income low and econ pressure high: grab more mexes
			elseif econPressure > 0.5 and goal and mincome < goal.m * 0.6
					and mexspot and SimpleT1Mexes[unitTeam] < TA.MEX_TARGET_MID then
				rung = "P3"
				AtMex(mexDef, mexspot)
				success = true

				-- PRIORITY MM: metal makers, when energy brims and metal is short
				-- (TA's way of turning a surplus of one into the other).
			elseif wantConverter and genRoom and nearHome and #converters > 0 then
				rung = "MM"
				if TryBuild(converters, function(p) SimpleBuildOrder(unitID, p) end) then
					SimpleConverterCount[unitTeam] = SimpleConverterCount[unitTeam] + 1
					success = true
				end

				-- PRIORITY 5 (late): the first factory when the energy bank was
				-- too low for it above.
			elseif SimpleFactoriesCount[unitTeam] == 0 and SimpleFactoryDelay[unitTeam] <= 0 then
				rung = "P5"
				if TryBuild(factories, function(p) SimpleBuildOrder(unitID, p) end, TA.AFFORD_FAC_SECS) then
					SimpleFactoryDelay[unitTeam] = 120
					SimpleLastFacStart[unitTeam] = nowFrame
					success = true
				end

				-- PRIORITY AS: a building of ours is half built and nobody is
				-- on it (its builder died, or it was shared to us): finish it.
			elseif assistOk and nanoframe then
				rung = "AS"
				Spring.GiveOrderToUnit(unitID, CMD.REPAIR, { nanoframe }, 0)
				success = true

				-- PRIORITY REP: something near us is hurt and nothing is
				-- shooting at it: repair it (TA has repair; SF did not).
			elseif repairOk and hurt then
				rung = "REP"
				Spring.GiveOrderToUnit(unitID, CMD.REPAIR, { hurt }, 0)
				success = true
				if STOR.DEBUG then
					local h, mh = Spring.GetUnitHealth(hurt)
					Spring.Echo(("[SimpleAI] team %d %s repairs %s (%d/%d)"):format(unitTeam, UnitDefs[unitDefID].name,
						UnitDefs[Spring.GetUnitDefID(hurt) or 0] and UnitDefs[Spring.GetUnitDefID(hurt)].name or "?", h or 0, mh or 0))
				end

				-- PRIORITY ST: the strategic behavior wants a silo or an
				-- anti-nuke (b_strategic decides when; it is built here).
			elseif stratWant and nearHome and CanMake(stratWant) then
				rung = "ST"
				success = SimpleBuildOrder(unitID, stratWant)

				-- PRIORITY 5a: ANTI-AIR — enemy aircraft were seen over the base
				-- or have hit us recently, and we are short of dedicated AA:
				-- raise it immediately. Outranks the generic reactive rung
				-- because when the attacker is a bomber, the generic slot's
				-- random pick is usually a turret that cannot shoot back.
			elseif needAA and buildType ~= "Commander" and #aaTurrets > 0 then
				rung = "5a"
				success = TryBuild(aaTurrets, function(p) SimpleBuildOrder(unitID, p) end)

				-- PRIORITY 5b: REACTIVE defense — if the base is under attack and we
				-- are under-defended, throw up a turret immediately (jumps the queue).
			elseif SimpleUnderAttack[unitTeam] and underDefended and canAffordTurret
					and buildType ~= "Commander" and #turrets > 0 then
				rung = "5b"
				success = TryBuild(turrets, function(p) SimpleBuildOrder(unitID, p) end)

				-- PRIORITY R: RECLAIM crew. A slot is open and wrecks are in
				-- reach: go and collect them. If no safe, unclaimed cell is in
				-- reach of THIS builder it falls through to building this tick
				-- (the open slot is left for a builder who is closer).
			elseif reclaimOk and STOR.Reclaim(unitID, unitTeam, nowFrame, recWM, recWE) then
				rung    = "R"
				success = true

				-- PRIORITY 5f: FORWARD defense. A few turrets at the team's most
				-- forward extractors and its muster point, on the side facing
				-- the enemy. Tried once per spacing window whether or not a
				-- site needed one, so it never holds a builder up.
			elseif forwardOk then
				rung = "5f"
				local ground = {}
				for _, id in ipairs(turrets) do
					if not IsAATurret[id] and CanMake(id) then ground[#ground + 1] = id end
				end
				if STOR.Forward(unitID, unitTeam, units, ground, techLevel, nowFrame) then
					success = true
				else
					-- nothing forward needs a turret (or no room there): do
					-- not ask again until the next window
					STOR.FWD.last[unitTeam] = nowFrame
				end

				-- PRIORITY 5c: OVERFLOW -> production. If resources are piling up, the
				-- single best thing to do is add a factory. This jumps ahead of mex
				-- expansion / generators / constructors / roaming so a surplus turns
				-- into production capacity fast instead of sitting in storage.
			elseif overflowing and nearHome and not stalling and SimpleFactoriesCount[unitTeam] > 0
					and facRoom and #factories > 0
					and facSpacingOk then
				rung = "5c"
				if TryBuild(factories, function(p) SimpleBuildOrder(unitID, p) end, TA.AFFORD_FAC_SECS) then
					SimpleLastFacStart[unitTeam] = nowFrame
					success = true
				end

				-- PRIORITY MOHO: a basic mex of ours upgraded in place (the moho
				-- goes on top, unit_mex_upgrade.lua removes the mex when it is
				-- done). Advanced builders only have mohos, so this is most of
				-- what they do for the economy. Never while stalling.
			elseif mohoDef and not stalling and ecurrent > epool * 0.35
					and not STOR.Hostile(unitTeam, unitposx, unitposz, mohoX, mohoZ) then
				rung = "MOHO"
				Spring.GiveOrderToUnit(unitID, -mohoDef, { mohoX, mohoY, mohoZ, 0 }, { "shift" })
				success = true

				-- PRIORITY 6b: STEADY defense — keep building toward the desired turret
				-- count. Gated by a coin-flip so it interleaves with expansion rather
				-- than monopolising the builder. (Builders only; commander keeps teching.)
			elseif underDefended and canAffordTurret and buildType ~= "Commander"
					and #turrets > 0 and math.random(0, 1) == 0 then
				rung = "6b"
				success = TryBuild(turrets, function(p) SimpleBuildOrder(unitID, p) end)

				-- PRIORITY 7: econ-biased generator building (to hit tech income target)
			elseif genRoom and nearHome and genPick and econPressure > 0.3 and goal and eincome < goal.e then
				rung = "P7"
				success = OrderPower(genPick)

				-- (PRIORITY 8, "builders build constructors", is gone: in TA
				-- constructors come from factories, see the FACTORY queue.)

				-- PRIORITY 11: roam to any unclaimed mex on the map (builders only)
				-- This fires before turrets so expansion always beats defense building.
			elseif mexAny and buildType ~= "Commander"
					and SimpleFactoriesCount[unitTeam] > 0
					and not STOR.Hostile(unitTeam, unitposx, unitposz, mexAny.x, mexAny.z) then
				rung = "P11"
				AtMex(mexAnyDef, mexAny)
				success = true

				-- PRIORITY 12: spare-time reclaim. A builder with nothing better
				-- to do collects wrecks too, crew slot or not (same targeting as
				-- rung R: a real cell in reach, never a blind sweep at the enemy
				-- base as this rung used to do).
			elseif buildType == "Builder" and reclaimUseful
					and STOR.Reclaim(unitID, unitTeam, nowFrame, recWM, recWE) then
				rung    = "P12"
				success = true

				-- PRIORITY 13: extra defense only if still under the desired count
				-- (steady/reactive slots above are the primary defense builders).
			elseif (r == 5 or r == 6) and underDefended and canAffordTurret and #turrets > 0 then
				rung = "P13"
				success = TryBuild(turrets, function(p) SimpleBuildOrder(unitID, p) end)

				-- FALLBACK: assist a factory, or a misc building
			else
				rung = "FB"
				-- Assist (TA has it): a builder with nothing better to do near
				-- home guards the busiest factory, which is what a player does
				-- with idle constructors. Capped by herd control ("as").
				if nearHome and assistOk and factoryToAssist and (buildType == "Commander" or math.random(0, 2) > 0) then
					rung = "FB.assist"
					Spring.GiveOrderToUnit(unitID, CMD.GUARD, { factoryToAssist }, 0)
					success = true
				end
				if not success and nearHome and #buildings > 0 and math.random(0, 1) == 0 then
					-- Misc buildings (radar, sonar, targeting facility, air
					-- repair pad) are worth having and worthless in bulk. Each
					-- type is capped by base size.
					local cap = math.min(STOR.SUPPORT_MAX,
						STOR.SUPPORT_BASE + math.floor((SimpleFactoriesCount[unitTeam] or 0) / STOR.SUPPORT_PER_FAC))
					local have = {}
					for i = 1, #units do
						local d = Spring.GetUnitDefID(units[i])
						if d and STOR.support[d] then have[d] = (have[d] or 0) + 1 end
					end
					local allowed = {}
					for _, id in ipairs(buildings) do
						if not STOR.support[id] or (have[id] or 0) < cap then
							allowed[#allowed + 1] = id
						end
					end
					success = TryBuild(allowed, function(p) SimpleBuildOrder(unitID, p) end)
				end
				-- If still no success and there are unclaimed mexes, go get one
				if not success and mexAny
						and not STOR.Hostile(unitTeam, unitposx, unitposz, mexAny.x, mexAny.z) then
					AtMex(mexAnyDef, mexAny)
					success = true
				end
				-- Out in the field with nothing left to do there: come home,
				-- where the base work is.
				if not success and not nearHome then
					local home = STOR.HomeOf(unitTeam)
					if home then
						rung = "home"
						local hx = home.x + math.random(-200, 200)
						local hz = home.z + math.random(-200, 200)
						Spring.GiveOrderToUnit(unitID, CMD.MOVE, { hx, Spring.GetGroundHeight(hx, hz), hz }, 0)
						success = true
					end
				end
			end

			-- -------------------------------------------------------
			-- FACTORY queue
			-- -------------------------------------------------------
		elseif buildType == "Factory" then
			-- A factory b_throttle has put on WAIT (stall relief) gets nothing
			-- new queued. While stalling the queue is kept short so the
			-- cheaper-unit preference takes effect right away instead of
			-- sitting behind ten pre-committed expensive units.
			local head = Spring.GetFactoryCommands(unitID, 1)
			if head and head[1] and head[1].id == CMD.WAIT then
				rung    = "F.wait"
				success = true
			elseif #Spring.GetFullBuildQueue(unitID, 0) == 0
					and (SimpleConstructorCount[unitTeam] or 0) < STOR.CON_EMERGENCY
					and conSpacingOk
					and TryBuild(constructors, function(p)
						local x, y, z = Spring.GetUnitPosition(unitID)
						Spring.GiveOrderToUnit(unitID, -p, { x, y, z, 0 }, 0)
					end) then
				-- Almost no builders left: one constructor goes to the head of
				-- an empty queue before anything else. (A factory with no
				-- constructor to offer falls through to its normal queue.)
				rung = "F.con"
				success = true
				SimpleLastConStart[unitTeam] = nowFrame
			elseif #Spring.GetFullBuildQueue(unitID, 0) < (stalling and STOR.STALL_QUEUE or 6)
					and unitRoom > 5 then
				local luaAI = Spring.GetTeamLuaAI(unitTeam)
				local isConAI = string.sub(luaAI, 1, 19) == 'SimpleConstructorAI'
				local conCap  = isConAI and CONSTRUCTOR_MAX_CON_AI or CONSTRUCTOR_MAX
				-- Two-part guard against worker floods:
				--   1. Hard cap: never exceed conCap live constructors.
				--   2. Spacing: only ONE constructor may START per team per window.
				-- Without (2) every factory evaluates in the same tick, all see the
				-- same stale count, and all queue a constructor at once. Dedicated
				-- SimpleConstructorAI teams skip the spacing (it's their whole job)
				-- but are still bounded by the higher cap.
				-- A rich reclaim field near home raises the builder cap by one
				-- per crew slot it could fill (up to REC.MAX): the extra hands
				-- are what a player queues up to clean a battlefield.
				local recNear = STOR.REC.near[unitTeam] or 0
				if recNear >= STOR.REC.RICH and not isConAI then
					conCap = conCap + math.min(STOR.REC.MAX, math.floor(recNear / STOR.REC.PER_BUILDER))
				end
				local haveConRoom = (SimpleConstructorCount[unitTeam] or 0) < conCap
				local wantConstructor = haveConRoom
						-- an energy stall is no time for a builder boom, but
						-- builders are also what ends it: never hold the team
						-- below STALL_CON_FLOOR (a recorded team stalled for ten
						-- minutes with one constructor because of exactly that)
						and (isConAI or not eStalling
							or (SimpleConstructorCount[unitTeam] or 0) < STOR.STALL_CON_FLOOR)
						and (isConAI or conSpacingOk)
						and (
							isConAI
							or math.random(0, 5) == 0
							or (SimpleConstructorCount[unitTeam] or 0) < 2 + 2 * (SimpleFactoriesCount[unitTeam] or 0)
							or econPressure > 0.4
							-- a rich reclaim field near home is worth extra hands
							or recNear >= STOR.REC.RICH )

				if wantConstructor then
					success = TryBuild(constructors, function(p)
						local x, y, z = Spring.GetUnitPosition(unitID)
						Spring.GiveOrderToUnit(unitID, -p, { x, y, z, 0 }, 0)
					end)
					if success then SimpleLastConStart[unitTeam] = nowFrame end
				end
				if not success then
					success = TryBuildWeighted(combats, function(p)
						local x, y, z = Spring.GetUnitPosition(unitID)
						Spring.GiveOrderToUnit(unitID, -p, { x, y, z, 0 }, 0)
					end)
				end
			else
				success = true
			end
		end

		-- Storage was wanted and this builder could have built it, but a
		-- higher rung took the builder instead. Say which signals were live.
		if STOR.DEBUG and storagePick and STOR.pending[unitTeam] ~= nowFrame
				and nowFrame >= (STOR.dbgAt[unitTeam] or 0) then
			STOR.dbgAt[unitTeam] = nowFrame + 900
			Spring.Echo(("[SimpleAI] storage: team %d tech %d wants %s but a higher rung took the builder"
				.. " (E %d/%d pool, E income %d, econPressure %.2f, underAttack %s)"):format(
				unitTeam, techLevel, UnitDefs[storagePick].name,
				ecurrent, epool, eincome, econPressure,
				tostring(SimpleUnderAttack[unitTeam] and true or false)))
		end

		-- Decision trace: count which rung took this unit, per team. The core
		-- publishes the tallies every 10s for the game recorder widget
		-- (dbg_game_recorder.lua). Keys: rung label, "C." prefix for the
		-- commander, "F" for a factory queue pick, "!" suffix when the rung
		-- was chosen but could not issue an order.
		-- Herd control: this unit now works for a capped need.
		local need = success and JOB.RUNG[rung]
		if need and jobs then
			jobs[unitID] = need
			active[need] = active[need] + 1
			if need == "gen" and genPick then
				-- so a second builder deciding in this same tick sees it
				active.genOut = (active.genOut or 0) + TA.EnergyOutput(UnitDefs[genPick])
			end
		end

		local tally = STOR.trace[unitTeam]
		if tally then
			-- "P2.cap": energy was wanted but enough builders were already on it
			if energyWanted and not genRoom and buildType ~= "Factory" then
				tally["P2.cap"] = (tally["P2.cap"] or 0) + 1
			end
			-- "fac.cap": the bank said "add a factory" and the factory limits said no
			if overflowing and nearHome and not stalling and facSpacingOk and not facRoom
					and buildType ~= "Factory" and SimpleFactoriesCount[unitTeam] > 0 then
				tally["fac.cap"] = (tally["fac.cap"] or 0) + 1
			end
			local key = rung
			if buildType == "Commander" then key = "C." .. key end
			if not success then
				key = key .. "!"
				if STOR.DEBUG and buildType ~= "Factory" then
					local n = 0
					for _, id in ipairs(factories) do if CanMake(id) then n = n + 1 end end
					Spring.Echo(("[SimpleAI] team %d %s failed rung %s (factories %d, canmake %d, bank M %d, income %.1f, brick=%s)"):format(
						unitTeam, UnitDefs[unitDefID].name, rung, #factories, n, mcurrent, mincome, tostring(lib.brickResult)))
				end
			end
			tally[key] = (tally[key] or 0) + 1
			if STOR.boOk   > 0 then tally["bo"]  = (tally["bo"]  or 0) + STOR.boOk   end
			if STOR.boFail > 0 then tally["bo!"] = (tally["bo!"] or 0) + STOR.boFail end
			if STOR.geoOk   > 0 then tally["geo"]  = (tally["geo"]  or 0) + STOR.geoOk   end
			if STOR.geoFail > 0 then   -- geo!.none / geo!.far / geo!.taken
				local key = "geo!." .. (STOR.geoWhy or "far")
				tally[key] = (tally[key] or 0) + STOR.geoFail
			end
		end
		STOR.boOk, STOR.boFail, STOR.geoOk, STOR.geoFail = 0, 0, 0, 0
		-- "unreach": sites turned down because they cannot be walked to from home
		if tally and lib.REACH then
			local st = lib.REACH.stats
			if st.no > (STOR.reachSeen or 0) then
				tally["unreach"] = (tally["unreach"] or 0) + (st.no - (STOR.reachSeen or 0))
			end
			STOR.reachSeen = st.no
		end
		-- brick planner: brick.slot (filled a slot), brick.new (planned a brick),
		-- brick.searching (still looking), brick.exhausted (no room in range)
		for result, count in pairs(STOR.brick) do
			if tally and count > 0 then
				tally["brick." .. result] = (tally["brick." .. result] or 0) + count
			end
			STOR.brick[result] = nil
		end

		return success
	end

	-- Shared service: the commander behavior builds through this too.
	services.SelectConstructionProject = SimpleConstructionProjectSelection

	--------------------------------------------------------------------------
	-- Storage and supply bookkeeping hooks. A finished storage (or one given to the
	-- team) releases the one-at-a-time lock; so does losing one, since the
	-- casualty may be the nanoframe the lock was waiting on.
	--------------------------------------------------------------------------
	-- Herd control recount (see JOB): a builder still counts toward its need
	-- only while the order at the head of its queue is a build order. Idle,
	-- dead, fleeing or reclaiming builders drop out here.
	function B.TeamTick(tick)
		local teamID = tick.teamID
		local jobs, active = JOB.of[teamID], JOB.active[teamID]
		if not jobs then return end
		active.gen, active.tur, active.rec, active.rep, active.as = 0, 0, 0, 0, 0
		active.genOut = 0   -- E/s of the plants builders are on their way to or building
		for unitID, need in pairs(jobs) do
			local queue = Spring.GetCommandQueue(unitID, 1)
			local head  = queue and queue[1]
			-- a reclaimer counts while it is reclaiming; everyone else while
			-- the order at the head of the queue is a build order
			local busy
			if need == "rec" then busy = head and head.id == CMD.RECLAIM
			elseif need == "rep" then busy = head and head.id == CMD.REPAIR
			elseif need == "as" then busy = head and (head.id == CMD.REPAIR or head.id == CMD.GUARD)
			else busy = head and head.id < 0 end
			if busy then
				active[need] = active[need] + 1
				if need == "gen" then
					local ud = UnitDefs[-head.id]
					active.genOut = active.genOut + EnergyOutput(ud)
				end
			else
				jobs[unitID] = nil
			end
		end

		-- Metal makers: off in an energy stall or with the bank nearly empty,
		-- on again once energy has recovered. One ONOFF sweep per change.
		do
			local eStall = (ctx.stall and ctx.stall.e[teamID]) or 0
			local eCur, eStor = tick.eCur or 0, tick.eStor or 1
			local wantOff = eStall >= (cfg.STALL_ON or 0.2) or eCur < eStor * MM.OFF_AT
			local wantOn  = eStall < (cfg.STALL_OFF or 0.08) and eCur > eStor * MM.ON_AT
			local isOff = MM.off[teamID] or false
			if (wantOff and not isOff) or (wantOn and isOff) then
				local units = tick.units
				local n = 0
				for i = 1, #units do
					local d = Spring.GetUnitDefID(units[i])
					if d and ctx.IsConverter and ctx.IsConverter[d] then
						Spring.GiveOrderToUnit(units[i], CMD.ONOFF, { wantOff and 0 or 1 }, 0)
						n = n + 1
					end
				end
				MM.off[teamID] = wantOff
				local tally = STOR.trace[teamID]
				if tally and n > 0 then
					local key = wantOff and "mm.off" or "mm.on"
					tally[key] = (tally[key] or 0) + n
				end
			end
		end

		-- Reclaim field: one scan serves every team; each team then sizes its
		-- crew from what lies within reach of its home.
		if tick.frame and (tick.frame - REC.lastScan) >= REC.SCAN then
			ReclaimScan(tick.frame)
		end
		ReclaimTeamUpdate(teamID, SimpleConstructorCount[teamID])

		if lib.ReachTick then lib.ReachTick(teamID) end   -- fresh path-request budget for this tick

		-- Reachability totals for the recording (GG.Recorder), every two
		-- minutes: how many questions were asked and how many refused.
		if GG.Recorder and GG.Recorder.Log and lib.REACH then
			local frame = tick.frame or 0
			if frame - (STOR.reachLogged[teamID] or 0) >= 3600 then
				STOR.reachLogged[teamID] = frame
				local st = lib.REACH.stats
				GG.Recorder.Log(teamID, "reach", ("asked=%d;no=%d;enabled=%s"):format(st.asked, st.no, lib.REACH.ENABLED and "1" or "0"))
			end
		end

		-- Brick planner: carry on any site search a builder is waiting for
		-- (see lib.BrickService), so builders rarely have to wait for one.
		local home = STOR.HomeOf(teamID)
		if home and lib.BrickService then
			local enemy = SimpleEnemyBasePos[teamID]
			lib.BrickService(teamID, home.x, home.z, enemy and enemy.x, enemy and enemy.z)
		end
	end

	function B.UnitFinished(unitID, unitDefID, unitTeam)
		if STOR.cap[unitDefID] then STOR.pending[unitTeam] = nil end
	end

	function B.UnitLost(unitTeam, unitID, unitDefID)
		SAFE.fleeAt[unitID] = nil
		SAFE.watch[unitID]  = nil
		if STOR.cap[unitDefID] then STOR.pending[unitTeam] = nil end
	end

	--------------------------------------------------------------------------
	-- Ownership: constructors and factories.
	--------------------------------------------------------------------------
	function B.unitFilter(unitDefID)
		return IsConstructor[unitDefID] == true or IsFactory[unitDefID] == true or IsAssistant[unitDefID] == true
	end

	-- Assistants (FARK, Necro: builders with nothing of their own to build).
	-- They repair whatever is hurt near the staging point or home, finish
	-- nanoframes, and otherwise guard the busiest factory. Enemies near:
	-- run home like a constructor.
	local function AssistantTick(tick, unitID, unitDefID, hpRatio, ux, uy, uz, unitCmds)
		local teamID = tick.teamID
		local nearEnemy = Spring.GetUnitNearestEnemy(unitID, SAFE.ALERT, true)
		if nearEnemy then
			local home = STOR.HomeOf(teamID)
			if home and unitCmds == 0 then
				Spring.GiveOrderToUnit(unitID, CMD.MOVE, { home.x, Spring.GetGroundHeight(home.x, home.z), home.z }, 0)
			end
			return
		end
		if unitCmds > 0 then return end
		-- hurt units near the muster point first (that is where the army waits)
		local muster = ctx.squad and ctx.squad.muster and ctx.squad.muster[teamID]
		local cx, cz = ux, uz
		local near = Spring.GetUnitsInCylinder(cx, cz, REPAIR_R, teamID)
		local best, bestScore = nil, 0
		local nano
		for i = 1, #near do
			local other = near[i]
			if other ~= unitID then
				local h, mh, _, _, bp = Spring.GetUnitHealth(other)
				if h and mh and mh > 0 then
					if (bp or 1) < 1 then
						nano = nano or other
					elseif h / mh < REPAIR_BELOW then
						local score = (1 - h / mh) * mh
						if score > bestScore then best, bestScore = other, score end
					end
				end
			end
		end
		if best then
			Spring.GiveOrderToUnit(unitID, CMD.REPAIR, { best }, 0)
		elseif nano then
			Spring.GiveOrderToUnit(unitID, CMD.REPAIR, { nano }, 0)
		elseif muster and ((ux - muster.x) ^ 2 + (uz - muster.z) ^ 2) > 500 * 500 and math.random(0, 1) == 0 then
			Spring.GiveOrderToUnit(unitID, CMD.MOVE, { muster.x + math.random(-120, 120), muster.y, muster.z + math.random(-120, 120) }, 0)
		else
			local units = tick.units
			local fac, facQ = nil, 0
			for i = 1, #units do
				local d = Spring.GetUnitDefID(units[i])
				if d and IsFactory[d] then
					local q = #(Spring.GetFullBuildQueue(units[i], 0) or {})
					if q > facQ then fac, facQ = units[i], q end
				end
			end
			if fac then Spring.GiveOrderToUnit(unitID, CMD.GUARD, { fac }, 0) end
		end
	end

	--------------------------------------------------------------------------
	-- Per-unit orders for constructors and factories.
	--------------------------------------------------------------------------
	function B.UnitTick(tick, unitID, unitDefID, hpRatio, ux, uy, uz, unitCmds)
		local teamID     = tick.teamID
		local allyTeamID = tick.allyTeamID
		local units      = tick.units
		local allunits   = tick.allUnits

		-- ======== ASSISTANTS ========
		if IsAssistant[unitDefID] then
			AssistantTick(tick, unitID, unitDefID, hpRatio, ux, uy, uz, unitCmds)

		-- ======== CONSTRUCTORS ========
		elseif IsConstructor[unitDefID] then

			-- Stuck-builder watchdog. A builder holding a build order that
			-- has neither moved nor started building for SAFE.STUCK frames
			-- is waiting on something that is not going to happen (a site
			-- that stays blocked, a spot it cannot reach). A recorded team
			-- ended its game with its last two builders frozen like that
			-- for eight minutes, at the supply cap, with 96,000 metal
			-- banked. The order is dropped so the builder decides again.
			do
				local w = SAFE.watch[unitID]
				local now = tick.frame or 0
				if not w then w = { x = ux, z = uz, since = now }; SAFE.watch[unitID] = w end
				local queue = (unitCmds > 0) and Spring.GetCommandQueue(unitID, 1)
				local head  = queue and queue[1]
				local dx, dz = ux - w.x, uz - w.z
				if not (head and head.id < 0)                         -- not holding a build order
						or (dx * dx + dz * dz) > SAFE.STUCK_MOVE * SAFE.STUCK_MOVE   -- it is getting somewhere
						or Spring.GetUnitIsBuilding(unitID) then      -- it is building
					w.x, w.z, w.since = ux, uz, now
				elseif (now - w.since) >= SAFE.STUCK then
					Spring.GiveOrderToUnit(unitID, CMD.STOP, {}, 0)
					w.x, w.z, w.since = ux, uz, now
					unitCmds = 0                                      -- it is idle as of now
					local tally = STOR.trace[teamID]
					if tally then tally["stuck"] = (tally["stuck"] or 0) + 1 end
				end
			end

			-- Enemy contact. A healthy builder used to answer ANY enemy within
			-- 600 elmos by walking up to reclaim it, armed or not, which is
			-- how most builders died (recordings: nearly every engineer built
			-- was lost, most of them far from home). Now:
			--   armed enemy near   -> run for home, and keep running
			--   unarmed enemy near -> reclaim it (free metal), if healthy
			local nearEnemy  = Spring.GetUnitNearestEnemy(unitID, SAFE.ALERT, true)
			local enemyArmed = false
			if nearEnemy then
				local eud = UnitDefs[Spring.GetUnitDefID(nearEnemy) or 0]
				enemyArmed = (eud and eud.weapons and #eud.weapons > 0) and true or false
			end

			if nearEnemy and (enemyArmed or hpRatio <= 0.85) then
				-- Run. Home if we know it and are not already there, else
				-- straight away from the enemy. Re-issued at most every
				-- SAFE.FLEE_REISSUE frames so the builder commits to a path
				-- instead of re-rolling a destination every tick.
				local now = tick.frame or 0
				if now >= (SAFE.fleeAt[unitID] or 0) then
					SAFE.fleeAt[unitID] = now + SAFE.FLEE_REISSUE
					local home = STOR.HomeOf(teamID)
					local tx, tz
					if home and ((home.x - ux) ^ 2 + (home.z - uz) ^ 2) > 600 * 600 then
						tx, tz = home.x, home.z
					else
						local ex, _, ez = Spring.GetUnitPosition(nearEnemy)
						local dx, dz = ux - (ex or ux), uz - (ez or uz)
						local d = math.sqrt(dx * dx + dz * dz)
						if d < 1 then dx, dz, d = 1, 0, 1 end
						tx = math.max(128, math.min(mapsizeX - 128, ux + dx / d * 900))
						tz = math.max(128, math.min(mapsizeZ - 128, uz + dz / d * 900))
					end
					Spring.GiveOrderToUnit(unitID, CMD.MOVE, { tx, Spring.GetGroundHeight(tx, tz), tz }, 0)
				end

			elseif nearEnemy then
				-- unarmed and we are healthy: take it apart
				Spring.GiveOrderToUnit(unitID, CMD.RECLAIM, { nearEnemy }, 0)

			elseif unitCmds == 0 then
				-- Check if we are very close to a factory (within its footprint).
				-- If so, walk away first before trying to build anything,
				-- otherwise SimpleBuildOrder will always fail.
				local tooClose = false
				for fi = 1, #units do
					local candidate = units[fi]
					if candidate ~= unitID then
						local cDefID = Spring.GetUnitDefID(candidate)
						if cDefID and IsFactory[cDefID] then
							local fx, _, fz = Spring.GetUnitPosition(candidate)
							local fdx, fdz = ux - fx, uz - fz
							local ffoot = math.max(
									UnitDefs[cDefID].xsize,
									UnitDefs[cDefID].zsize) * 8 + 200
							if fdx * fdx + fdz * fdz < ffoot * ffoot then
								tooClose = true
								-- Walk in a random direction away from the factory
								local angle = math.random() * 6.28
								local dist  = ffoot + math.random(200, 500)
								local wx = fx + math.cos(angle) * dist
								local wz = fz + math.sin(angle) * dist
								wx = math.max(256, math.min(mapsizeX - 256, wx))
								wz = math.max(256, math.min(mapsizeZ - 256, wz))
								local wy = Spring.GetGroundHeight(wx, wz)
								Spring.GiveOrderToUnit(unitID, CMD.MOVE, { wx, wy, wz }, 0)
								break
							end
						end
					end
				end

				if not tooClose then
					SimpleConstructionProjectSelection(
							unitID, unitDefID, teamID, allyTeamID,
							units, allunits, "Builder")
				end
			end

			-- ======== FACTORIES ========
		else
			if unitCmds == 0 then
				SimpleConstructionProjectSelection(
						unitID, unitDefID, teamID, allyTeamID,
						units, allunits, "Factory")
			end
		end
	end

	return B
end
