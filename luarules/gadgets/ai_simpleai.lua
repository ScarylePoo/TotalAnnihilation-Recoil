--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--
--  file:    luarules/gadgets/ai_simpleai.lua
--  brief:   SimpleAI / AdaptiveAI core for TA:Recoil. Ported from Splinter
--           Faction's SimpleAI Enhanced (Damgam 2020, SF v3-v6): the core
--           classifies units, keeps the per-team counters and the shared
--           context (ctx), runs the per-team tick, and dispatches to the
--           behavior modules in luarules/configs/simpleai/behaviors/.
--
--           What is different from SF (see tools/ta-data/HANDOFF.md, "AI"):
--             * factions are ARM / CORE, read from the unit name prefix
--             * tech is not a commander morph: a unit's tier is in its name
--               (_t1_/_t2_/_t3_) and a team's tech level is the highest tier
--               any of its builders can build (a T1 constructor can build an
--               Advanced lab, so it counts as tech 2)
--             * no research points, build boosts, morphs or supply cap
--             * ships are their own class (IsShip); hovercraft are ground
--             * assistants (FARK, Necro: builders with no build list) are a
--               class of their own, used to repair and assist
--             * stockpile silos (nukes, EMP) and anti-nukes are "strategic",
--               long-range plasma is "lrpc": neither is a turret
--
--  license: GNU GPL, v2 or later
--
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

local enabled        = false
local teams          = Spring.GetTeamList()
local mapsizeX       = Game.mapSizeX
local mapsizeZ       = Game.mapSizeZ
local gaiaTeamID     = Spring.GetGaiaTeamID()

-- ============================================================
-- CONSTANTS
-- ============================================================

local WAVE_INTERVAL     = 3600   -- frames between attack wave launches (legacy: attackTimer init only)

-- Combat composition. Multiplies a unit's build weight by its role so the AI
-- leans on the front-line units while still fielding support. Keyed by the
-- role glyph of the unit's radar icon (gamedata/unit_icons.lua: kbot_light_t1
-- -> "light"), which is the one place every unit's role is already written down.
local COMBAT_ROLE_WEIGHT = {
	light     = 1.00,   -- raiders and infantry: the bread and butter
	assault   = 1.00,
	heavy     = 0.90,
	artillery = 0.50,
	rocket    = 0.60,
	aa        = 0.30,   -- x AA_THREAT_MULT while enemy air is about (lib.CombatRoleWeight)
	bomber    = 0.80,
	torpedo   = 0.30,
	sniper    = 0.35,
	emp       = 0.30,
	kamikaze  = 0.15,
	scout     = 0.15,
	radar     = 0.10,
	sonar     = 0.10,
	jammer    = 0.10,
	spy       = 0.05,
	carrier   = 0.20,
	default   = 0.60,   -- anything with no/unknown role
	AA_THREAT_MULT = 3.0,
	-- Ceiling for units that cannot kill: every weapon is a paralyzer (the
	-- Spider, the Stunner). Detected from the weapon defs (lib.NonDirectClass).
	DisruptOnly = 0.25,
}

-- Weak-point attack targeting
local ATTACK_SCAN_R     = 650    -- radius around an enemy building used to tally its defenders
local ATTACK_DIST_W     = 0.10   -- how strongly distance-from-muster penalises a candidate target

local FACTORY_OVERFLOW      = 0.62 -- metal & energy signal-pool fraction that counts as "overflowing"

-- Signal pool (see SF): thresholds are measured against SIGNAL_POOL_SECONDS of
-- income, never below the stock pool, never above real storage.
local SIGNAL_POOL_MIN     = 1000
local SIGNAL_POOL_SECONDS = 20
local function SignalPool(storage, income)
	local pool = (income or 0) * SIGNAL_POOL_SECONDS
	if pool < SIGNAL_POOL_MIN then pool = SIGNAL_POOL_MIN end
	if pool > storage then pool = storage end
	return pool
end

-- Stall signal (see SF): raw stall = 1 - income / pull when demand outruns income
-- and the bank is empty; smoothed; metal discounted (an AI that spends everything
-- always wants more metal; an energy stall can be fixed by building cheaper).
local STALL_STOCK_SECONDS = 3
local STALL_SMOOTH        = 0.35
local STALL_ON            = 0.20
local STALL_OFF           = 0.08
local STALL_HARD          = 0.45
local STALL_METAL_WEIGHT  = 0.5
local function StallStep(prev, current, pull, income)
	local raw = 0
	if pull and pull > 0 and pull > income and current < pull * STALL_STOCK_SECONDS then
		raw = 1 - income / pull
	end
	return prev + (raw - prev) * STALL_SMOOTH
end

-- Commander lost (TA: the team is out when its last commander dies in the
-- default game modes, but with "killall" it plays on without one).
local COMM_LOST_GRACE     = 300
local commSeen            = {}
local commGoneAt          = {}

-- Decision trace: every TRACE_INTERVAL frames each AI team publishes one
-- string to the team rules param "simpleai_trace" (and the infolog when
-- debugmode is on).
local TRACE_INTERVAL      = 300
local traceLast           = {}
local traceAttacked       = {}
local traceTicks          = {}
local traceKeys           = {}
local TRACE_ECHO = tostring((Spring.GetModOptions() or {}).aitrace or "0") ~= "0"

-- Resource floor (NeverStall): every second a covered team's stock is topped up
-- to NEVERSTALL_FLOOR of a FIXED base (the stock 1k pool), i.e. 150. Coverage:
-- AdaptiveAI always (throughput is steered by build speed, stalling must not be
-- a variable for the controller); plain SimpleAI only with the ai_neverstall
-- modoption.
local NEVERSTALL_FLOOR = 0.15
local NEVERSTALL_BASE  = 1000
local neverstallOn = tostring((Spring.GetModOptions() or {}).ai_neverstall or "enabled") ~= "disabled"

-- ============================================================
-- SHARED AI CONTEXT (ctx): all shared mutable state. Behaviors see only this.
-- ============================================================
local ctx = {
	aiTeams      = {},
	isAITeam     = {},
	adaptiveTeams = {},

	-- unit classification (defID-keyed, immutable after load)
	IsCommander = {}, IsFactory = {}, IsConstructor = {}, IsExtractor = {},
	IsCombat    = {}, IsConverter = {}, IsTurret = {}, IsAir = {},
	IsAATurret  = {},
	IsShip      = {},   -- [defID] = true: ship or submarine (own combat handling)
	IsAssistant = {},   -- [defID] = true: mobile builder with no build list (FARK, Necro): repairs and assists
	IsSilo      = {},   -- [defID] = true: stockpile weapon that is not an interceptor (nuke, EMP launcher)
	IsAntiNuke  = {},   -- [defID] = true: interceptor
	IsLRPC      = {},   -- [defID] = true: long-range plasma (Big Bertha, Intimidator, Vulcan, Buzzsaw)
	IsAirFactory = {}, IsSeaFactory = {},   -- [factoryDefID] = true
	Tier        = {},   -- [defID] = 1..3 from the unit name
	BuilderTier = {},   -- [defID] = highest tier the def can build (0 = nothing)
	Role        = {},   -- [defID] = radar icon role glyph ("light", "aa", ...)
	ShieldMax   = {},   -- [defID] = personal shield capacity (optional shields gadget)
	BoostCost   = {},   -- (SF; unused)
	commanderDefs = {}, factoryDefs = {}, constructorDefs = {},
	extractorDefs = {}, undefinedDefs = {},

	trace = {},
	stall = { m = {}, e = {}, v = {}, paused = {} },
	home = {},
	defCat = {},
	reclaim = { near = {} },

	counters = {
		factories = {}, factoriesByDef = {}, mexes = {}, constructors = {},
		army = {}, converters = {}, turrets = {}, landFactories = {},
		aaTurrets = {}, airFactories = {}, seaFactories = {},
		tierBuilders = {},   -- [teamID][tier] = builders alive that can build that tier
	},
	pacing = {
		factoryDelay = {}, constructorDelay = {},
		lastConStart = {}, lastFacStart = {},
		lastLaunch = {}, lastTargetScan = {}, lastBoost = {},
	},
	squad   = { muster = {}, state = {}, attackWave = {}, attackTimer = {} },
	intel   = { underAttack = {}, enemyBase = {}, baseThreat = {}, airThreat = {} },
	comm    = { retreating = {}, retreatPos = {}, id = {}, lost = {} },
	techLevel  = {},   -- 1-3 per team
	faction    = {},   -- "arm" | "core" per team
	buildLists = {},   -- [teamID][tier][category] = {defID, ...}

	retreat = {},
	tick = {},
}

local SimpleAITeamIDs             = ctx.aiTeams
local SimpleAITeamIDsCount        = 0
local IsAITeamID                  = ctx.isAITeam
local AdaptiveTeams               = ctx.adaptiveTeams

SimpleFactoriesCount   = ctx.counters.factories
SimpleFactories        = ctx.counters.factoriesByDef
SimpleT1Mexes          = ctx.counters.mexes
SimpleConstructorCount = ctx.counters.constructors
SimpleFactoryDelay     = ctx.pacing.factoryDelay
SimpleConstructorDelay = ctx.pacing.constructorDelay
SimpleLastConStart     = ctx.pacing.lastConStart
SimpleLastFacStart     = ctx.pacing.lastFacStart

local SimpleArmyCount      = ctx.counters.army
local SimpleAttackTimer    = ctx.squad.attackTimer
local SimpleUnderAttack    = ctx.intel.underAttack
local SimpleEnemyBasePos   = ctx.intel.enemyBase
local SimpleConverterCount = ctx.counters.converters
local SimpleTurretCount    = ctx.counters.turrets
local SimpleAATurretCount  = ctx.counters.aaTurrets
local SimpleLandFacCount   = ctx.counters.landFactories
local SimpleAirThreat      = ctx.intel.airThreat
local SimpleCommRetreating = ctx.comm.retreating
local SimpleCommRetreatPos = ctx.comm.retreatPos
local SimpleRetreatState   = ctx.retreat
local TeamTechLevel  = ctx.techLevel
local TeamFaction    = ctx.faction
local TeamCommID     = ctx.comm.id
local TeamBuildLists = ctx.buildLists
local TierBuilders   = ctx.counters.tierBuilders

local CATEGORIES = { "extractor", "generator", "converter", "turret", "storage", "factory",
                     "constructor", "combat", "building", "strategic" }
local MAX_TIER = 3

-- ============================================================
-- HELPERS
-- ============================================================

-- The tier written in the unit's name: arm_t2_bot_zeus -> 2. Commanders and
-- anything without one count as tier 1.
local function TierOf(ud)
	local t = ud and ud.name and string.match(ud.name, "_t(%d)_")
	t = t and tonumber(t) or 1
	if t < 1 then t = 1 elseif t > MAX_TIER then t = MAX_TIER end
	return t
end

local function FactionOf(ud)
	local n = ud and ud.name or ""
	if string.sub(n, 1, 4) == "arm_" then return "arm" end
	if string.sub(n, 1, 5) == "core_" then return "core" end
	return nil
end

-- ============================================================
-- INITIALISE TEAM RECORDS
-- ============================================================
for i = 1, #teams do
	local teamID = teams[i]
	local luaAI  = Spring.GetTeamLuaAI(teamID)
	local isAdaptive = luaAI ~= nil and luaAI ~= ""
			and string.sub(luaAI, 1, 10) == 'AdaptiveAI'
	if luaAI and luaAI ~= "" and (
			isAdaptive or
					string.sub(luaAI, 1, 8)  == 'SimpleAI' or
					string.sub(luaAI, 1, 16) == 'SimpleDefenderAI' or
					string.sub(luaAI, 1, 19) == 'SimpleConstructorAI'
	) then
		enabled = true
		if isAdaptive then
			AdaptiveTeams[teamID] = true
		end
		SimpleAITeamIDsCount = SimpleAITeamIDsCount + 1
		SimpleAITeamIDs[SimpleAITeamIDsCount] = teamID
		IsAITeamID[teamID] = true

		SimpleFactoriesCount[teamID]   = 0
		SimpleFactories[teamID]        = {}
		SimpleT1Mexes[teamID]          = 0
		SimpleConstructorCount[teamID] = 0
		SimpleArmyCount[teamID]        = 0
		SimpleAttackTimer[teamID]      = WAVE_INTERVAL
		SimpleUnderAttack[teamID]      = false
		SimpleEnemyBasePos[teamID]     = nil
		SimpleConverterCount[teamID]   = 0
		SimpleTurretCount[teamID]      = 0
		SimpleAATurretCount[teamID]    = 0
		SimpleLandFacCount[teamID]     = 0
		ctx.counters.airFactories[teamID] = 0
		ctx.counters.seaFactories[teamID] = 0
		TierBuilders[teamID]           = { 0, 0, 0 }
		SimpleAirThreat[teamID]        = nil
		TeamTechLevel[teamID]          = 1
		ctx.trace[teamID]              = {}
		ctx.stall.m[teamID], ctx.stall.e[teamID] = 0, 0
		ctx.stall.v[teamID], ctx.stall.paused[teamID] = 0, 0
		TeamFaction[teamID]            = nil
		TeamCommID[teamID]             = nil
		TeamBuildLists[teamID]         = {}
		for t = 0, MAX_TIER do
			TeamBuildLists[teamID][t] = {}
			for _, cat in ipairs(CATEGORIES) do TeamBuildLists[teamID][t][cat] = {} end
		end
	end
end

-- ============================================================
-- GADGET INFO
-- ============================================================
function gadget:GetInfo()
	return {
		name    = "SimpleAI",
		desc    = "SimpleAI + AdaptiveAI (real-time difficulty) for TA:Recoil, ported from Splinter Faction",
		author  = "Damgam / SF Enhanced v6 / TA:Recoil port",
		date    = "2026",
		layer   = -100,
		enabled = enabled,
	}
end

-- ============================================================
-- UNIT-TYPE IDENTIFICATION
-- ============================================================
local IsCommander   = ctx.IsCommander
local IsFactory     = ctx.IsFactory
local IsConstructor = ctx.IsConstructor
local IsExtractor   = ctx.IsExtractor
local IsCombat      = ctx.IsCombat
local IsConverter   = ctx.IsConverter
local IsTurret      = ctx.IsTurret
local IsAir         = ctx.IsAir
local IsAATurret    = ctx.IsAATurret
local IsShip        = ctx.IsShip
local IsAssistant   = ctx.IsAssistant
local IsSilo        = ctx.IsSilo
local IsAntiNuke    = ctx.IsAntiNuke
local IsLRPC        = ctx.IsLRPC
local IsAirFactory  = ctx.IsAirFactory
local IsSeaFactory  = ctx.IsSeaFactory

-- A weapon that may target only aircraft: in TA the FBI's toairweapon / the
-- VTOL-only target category. The Lua UnitDefs proxy shows it as
-- weapons[i].onlyTargets = { vtol = true } (one key). Weapons that hit ground
-- too list every category.
local function HasAAOnlyWeapon(unitDef)
	local weps = unitDef.weapons
	if not weps then return false end
	for i = 1, #weps do
		local ot = weps[i].onlyTargets
		if ot and (ot.vtol or ot.air) and next(ot, next(ot)) == nil then
			return true
		end
	end
	return false
end

-- Stockpile weapons: interceptor = anti-nuke, else a silo (nuke, EMP missile).
local function StockpileKind(unitDef)
	local weps = unitDef.weapons
	if not weps then return nil end
	for i = 1, #weps do
		local wd = WeaponDefs[weps[i].weaponDef]
		if wd and wd.stockpile then
			if (wd.interceptor or 0) > 0 then return "antinuke" end
			return "silo"
		end
	end
	return nil
end

local LRPC_RANGE = 2000   -- a building weapon with more range than this is artillery, not a turret
local function MaxWeaponRange(unitDef)
	local r = 0
	for i = 1, #(unitDef.weapons or {}) do
		local wd = WeaponDefs[unitDef.weapons[i].weaponDef]
		if wd and wd.range and wd.range > r then r = wd.range end
	end
	return r
end

-- Mine layers (the Podger, the Spoiler) build nothing but mines: not a
-- constructor the AI should buy or send to build. Left as an assistant.
local function OnlyMines(ud)
	for _, opt in ipairs(ud.buildOptions or {}) do
		local od = UnitDefs[opt]
		if od and not od.canKamikaze then return false end
	end
	return true
end

local function IsWall(ud)
	local n = ud.name or ""
	return n:find("dragonsteeth", 1, true) or n:find("fortificationwall", 1, true)
end

local SimpleCommanderDefs     = ctx.commanderDefs
local SimpleFactoriesDefs     = ctx.factoryDefs
local SimpleConstructorDefs   = ctx.constructorDefs
local SimpleExtractorDefs     = ctx.extractorDefs
local SimpleUndefinedUnitDefs = ctx.undefinedDefs

local unitIcons = VFS.Include("gamedata/unit_icons.lua") or {}

for unitDefID, unitDef in pairs(UnitDefs) do
	local cp = unitDef.customParams or {}
	ctx.Tier[unitDefID] = TierOf(unitDef)
	local icon = unitIcons[unitDef.name]
	if icon then
		local glyph = string.match(icon, "^[a-z]+_([a-z_]-)_t%d") or string.match(icon, "^[a-z]+_([a-z_]+)$")
		if glyph and glyph:sub(1, 2) == "f_" then glyph = nil end
		ctx.Role[unitDefID] = glyph
	end
	local md = unitDef.moveDef
	if md and md.smClass == 3 then IsShip[unitDefID] = true end
	if unitDef.canFly then IsAir[unitDefID] = true end

	if cp.iscommander then
		IsCommander[unitDefID] = true
		SimpleCommanderDefs[#SimpleCommanderDefs + 1] = unitDefID

	elseif unitDef.isFactory and #unitDef.buildOptions > 0 then
		IsFactory[unitDefID] = true
		SimpleFactoriesDefs[#SimpleFactoriesDefs + 1] = unitDefID
		local allAir, anySea = true, false
		for _, opt in ipairs(unitDef.buildOptions) do
			local od = UnitDefs[opt]
			if od and not od.canFly then allAir = false end
			if od and od.moveDef and od.moveDef.smClass == 3 then anySea = true end
		end
		if allAir then IsAirFactory[unitDefID] = true end
		if anySea or (unitDef.minWaterDepth or 0) > 0 then IsSeaFactory[unitDefID] = true end

	elseif unitDef.canMove and unitDef.isBuilder and #unitDef.buildOptions > 0 and not OnlyMines(unitDef) then
		IsConstructor[unitDefID] = true
		SimpleConstructorDefs[#SimpleConstructorDefs + 1] = unitDefID

	elseif unitDef.canMove and unitDef.isBuilder and (unitDef.canRepair or unitDef.canAssist or unitDef.canResurrect) then
		IsAssistant[unitDefID] = true   -- (mine layers end up here too; they are never put on a build list)

	elseif unitDef.extractsMetal > 0 or cp.metal_spot_mult then
		-- (TA:Recoil mexes are metal makers on fixed spots: game_metal_spots.lua
		-- tags them with customparams.metal_spot_mult and may zero extractsMetal)
		IsExtractor[unitDefID] = true
		SimpleExtractorDefs[#SimpleExtractorDefs + 1] = unitDefID

	elseif unitDef.isBuilding and (unitDef.makesMetal or 0) > 0 then
		IsConverter[unitDefID] = true

	elseif unitDef.isBuilding and unitDef.weapons and #unitDef.weapons > 0 then
		local kind = StockpileKind(unitDef)
		if kind == "antinuke" then
			IsAntiNuke[unitDefID] = true
		elseif kind == "silo" then
			IsSilo[unitDefID] = true
		elseif MaxWeaponRange(unitDef) > LRPC_RANGE then
			IsLRPC[unitDefID] = true
		else
			IsTurret[unitDefID] = true
			if HasAAOnlyWeapon(unitDef) then
				IsAATurret[unitDefID] = true
			end
		end

	elseif unitDef.canMove and not unitDef.isBuilder and #(unitDef.weapons or {}) > 0 then
		IsCombat[unitDefID] = true
		SimpleUndefinedUnitDefs[#SimpleUndefinedUnitDefs + 1] = unitDefID
	end

	-- the highest tier this def can build (0: nothing)
	local bt = 0
	for _, opt in ipairs(unitDef.buildOptions or {}) do
		local t = TierOf(UnitDefs[opt])
		if t > bt then bt = t end
	end
	ctx.BuilderTier[unitDefID] = bt
end

-- Personal shields (luarules/gadgets/unit_protoss_style_shields.lua; no TA
-- unit has one, modders may): EFFECTIVE hp = hull + shield.
local ShieldMax = ctx.ShieldMax
for unitDefID, unitDef in pairs(UnitDefs) do
	local cp = unitDef.customParams or {}
	if cp.isshieldedunit == "1" then
		ShieldMax[unitDefID] = tonumber(cp.shield_max_strength) or 100
	end
end

-- ============================================================
-- HELPER LIBRARY
-- ============================================================
local sharedCfg = {
	mapsizeX           = mapsizeX,
	mapsizeZ           = mapsizeZ,
	gaiaTeamID         = gaiaTeamID,
	ATTACK_SCAN_R      = ATTACK_SCAN_R,
	ATTACK_DIST_W      = ATTACK_DIST_W,
	COMBAT_ROLE_WEIGHT = COMBAT_ROLE_WEIGHT,
	FACTORY_OVERFLOW   = FACTORY_OVERFLOW,
	SignalPool         = SignalPool,
	STALL_ON           = STALL_ON,
	STALL_OFF          = STALL_OFF,
	STALL_HARD         = STALL_HARD,
	TRACE_ECHO         = TRACE_ECHO,
}
local lib = VFS.Include("luarules/configs/simpleai/lib.lua")(ctx, sharedCfg)

local EffectiveRatio          = lib.EffectiveRatio
local EstimateEnemyBase       = lib.EstimateEnemyBase

-- ============================================================
-- BEHAVIOR MODULES
-- Each returns function(ctx, lib, cfg, services) -> handler table with
-- name, order, unitFilter, TeamInit, TeamTick, UnitTick and event hooks.
-- ============================================================
local BEHAVIOR_FILES = {
	"luarules/configs/simpleai/behaviors/b_adaptive.lua",      -- order 5; difficulty controller, registers GetKnobs
	"luarules/configs/simpleai/behaviors/b_defense.lua",       -- order 10 (intel first)
	"luarules/configs/simpleai/behaviors/b_construction.lua",  -- order 40; registers services
	"luarules/configs/simpleai/behaviors/b_commander.lua",     -- order 20; consumes services
	"luarules/configs/simpleai/behaviors/b_throttle.lua",      -- order 32; pauses/cancels factory work while stalling
	"luarules/configs/simpleai/behaviors/b_strategic.lua",     -- order 36; nukes and anti-nukes
	"luarules/configs/simpleai/behaviors/b_combat.lua",        -- order 50
	"luarules/configs/simpleai/behaviors/b_surrender.lua",     -- order 90; gg and self-destruct when the game is obviously lost
}

local services  = {}
local behaviors = {}
if gadgetHandler:IsSyncedCode() then
	for i = 1, #BEHAVIOR_FILES do
		behaviors[#behaviors + 1] = VFS.Include(BEHAVIOR_FILES[i])(ctx, lib, sharedCfg, services)
	end
	table.sort(behaviors, function(a, b)
		return (a.order or 100) < (b.order or 100)
	end)
	for bi = 1, #behaviors do
		local b = behaviors[bi]
		if b.TeamInit then
			for ti = 1, #ctx.aiTeams do
				b.TeamInit(ctx.aiTeams[ti])
			end
		end
	end
end

local unitOwnerCache = {}
local function OwnerOf(unitDefID)
	local owner = unitOwnerCache[unitDefID]
	if owner == nil then
		owner = false
		for i = 1, #behaviors do
			local b = behaviors[i]
			if b.unitFilter and b.unitFilter(unitDefID) then
				owner = b
				break
			end
		end
		unitOwnerCache[unitDefID] = owner
	end
	return owner
end

-- ============================================================
-- BUILD LIST POPULATION
-- Once per team when its faction is known: every def of the faction sorted
-- into per-tier, per-category buckets. Tier gating happens at read time
-- (lib.GetBuildable, against ctx.techLevel).
-- ============================================================
local function PopulateBuildLists(teamID, faction)
	local lists = TeamBuildLists[teamID]
	for t = 0, MAX_TIER do
		for _, cat in ipairs(CATEGORIES) do lists[t][cat] = {} end
	end

	for unitDefID, unitDef in pairs(UnitDefs) do
		if FactionOf(unitDef) == faction then
			local tier = ctx.Tier[unitDefID]
			local cat  = nil
			local name = unitDef.name or ""

			if IsCommander[unitDefID] or name:find("decoycommander", 1, true) then
				cat = nil   -- never on a build list
			elseif IsExtractor[unitDefID] then
				cat = "extractor"
			elseif IsFactory[unitDefID] then
				cat = "factory"
			elseif IsConstructor[unitDefID] or (IsAssistant[unitDefID] and not OnlyMines(unitDef)) then
				cat = "constructor"   -- (before generators: TA's builders make energy too)
			elseif unitDef.isBuilding and lib.EnergyOutput(unitDef) > 0 then
				cat = "generator"
			elseif IsConverter[unitDefID] then
				cat = "converter"
			elseif IsTurret[unitDefID] then
				cat = "turret"
			elseif IsSilo[unitDefID] or IsAntiNuke[unitDefID] or IsLRPC[unitDefID] then
				cat = "strategic"
			elseif unitDef.isBuilding and ((unitDef.metalStorage or 0) > 0 or (unitDef.energyStorage or 0) > 0) then
				cat = "storage"
			elseif unitDef.isBuilding then
				-- radar, sonar, targeting facility, air repair pad...; not walls or mines
				if not IsWall(unitDef) and not unitDef.canKamikaze then cat = "building" end
			elseif IsCombat[unitDefID] then
				cat = "combat"
			end

			if cat then
				ctx.defCat[unitDefID] = cat
				local bucket = lists[tier][cat]
				if bucket then bucket[#bucket + 1] = unitDefID end
			end
		end
	end
	for t = 0, MAX_TIER do
		for _, cat in ipairs(CATEGORIES) do table.sort(lists[t][cat]) end
	end
end

-- Team tech level: the highest tier any living builder of the team can build.
local function RecomputeTech(teamID)
	local tb = TierBuilders[teamID]
	local tech = 1
	for t = MAX_TIER, 1, -1 do
		if (tb[t] or 0) > 0 then tech = t; break end
	end
	TeamTechLevel[teamID] = tech
end

-- ============================================================
-- LIFECYCLE
-- ============================================================
function gadget:GameOver()
	gadgetHandler:RemoveGadget(self)
end

if gadgetHandler:IsSyncedCode() then

	function gadget:GameFrame(n)

		-- Resource floor (see NEVERSTALL_FLOOR). Frame offset 27 keeps it off
		-- the %15==0 AI-tick frames.
		if n % 30 == 27 then
			for j = 1, SimpleAITeamIDsCount do
				local teamID = SimpleAITeamIDs[j]
				if AdaptiveTeams[teamID] or neverstallOn then
					local mc, ms = Spring.GetTeamResources(teamID, "metal")
					local ec, es = Spring.GetTeamResources(teamID, "energy")
					if mc then
						local mFloor = math.min(ms, NEVERSTALL_BASE) * NEVERSTALL_FLOOR
						if mc < mFloor then
							Spring.SetTeamResource(teamID, "m", mFloor)
						end
					end
					if ec then
						local eFloor = math.min(es, NEVERSTALL_BASE) * NEVERSTALL_FLOOR
						if ec < eFloor then
							Spring.SetTeamResource(teamID, "e", eFloor)
						end
					end
				end
			end
		end

		-- Update enemy base estimate every ~20s
		if n % 1200 == 0 then
			for i = 1, SimpleAITeamIDsCount do
				SimpleEnemyBasePos[SimpleAITeamIDs[i]] =
				EstimateEnemyBase(SimpleAITeamIDs[i])
			end
		end

		-- Main per-unit loop (staggered across teams)
		if n % 15 == 0 then
			for i = 1, SimpleAITeamIDsCount do
				if n % (15 * SimpleAITeamIDsCount) == 15 * (i - 1) then

					local teamID = SimpleAITeamIDs[i]
					local _, _, isDead, _, _, allyTeamID = Spring.GetTeamInfo(teamID)
					local mcurrent, mstorage, mpull, mincome = Spring.GetTeamResources(teamID, "metal")
					local ecurrent, estorage, epull, eincome = Spring.GetTeamResources(teamID, "energy")
					local units    = Spring.GetTeamUnits(teamID)
					local allunits = Spring.GetAllUnits()
					local luaAI    = Spring.GetTeamLuaAI(teamID)

					local tick     = ctx.tick
					tick.frame     = n
					tick.teamID    = teamID
					tick.allyTeamID = allyTeamID
					tick.units     = units
					tick.allUnits  = allunits
					tick.mCur, tick.mStor, tick.mInc = mcurrent, mstorage, mincome
					tick.eCur, tick.eStor, tick.eInc = ecurrent, estorage, eincome
					tick.mPull, tick.ePull = mpull, epull
					local mpool = SignalPool(mstorage, mincome)
					local epool = SignalPool(estorage, eincome)
					tick.mPool, tick.ePool = mpool, epool
					tick.overflowing = mstorage > 0 and estorage > 0
							and mcurrent > mpool * FACTORY_OVERFLOW
							and ecurrent > epool * FACTORY_OVERFLOW
					tick.luaAI = luaAI

					-- Commander lost? (see COMM_LOST_GRACE)
					if TeamCommID[teamID] then
						commSeen[teamID], commGoneAt[teamID] = true, nil
						ctx.comm.lost[teamID] = false
					elseif commSeen[teamID] then
						commGoneAt[teamID] = commGoneAt[teamID] or n
						if n - commGoneAt[teamID] >= COMM_LOST_GRACE then
							ctx.comm.lost[teamID] = true
						end
					end

					-- Stall signal (see StallStep above).
					local stall  = ctx.stall
					local mStall = StallStep(stall.m[teamID] or 0, mcurrent, mpull, mincome)
					local eStall = StallStep(stall.e[teamID] or 0, ecurrent, epull, eincome)
					stall.m[teamID], stall.e[teamID] = mStall, eStall
					local mWeighted = mStall * STALL_METAL_WEIGHT
					stall.v[teamID] = (mWeighted > eStall) and mWeighted or eStall
					tick.mStall, tick.eStall, tick.stall = mStall, eStall, stall.v[teamID]

					for bi = 1, #behaviors do
						local b = behaviors[bi]
						if b.TeamTick then b.TeamTick(tick) end
					end

					for k = 1, #units do
						local unitID    = units[k]
						local unitDefID = Spring.GetUnitDefID(unitID)
						local unitHealth, unitMaxHealth = Spring.GetUnitHealth(unitID)

						if unitDefID and unitHealth then
							local hpRatio    = EffectiveRatio(unitID, unitDefID,
							                                  unitHealth, unitMaxHealth)
							local ux, uy, uz = Spring.GetUnitPosition(unitID)
							local unitCmds   = Spring.GetCommandQueue(unitID, 0)

							local owner = OwnerOf(unitDefID)
							if owner and owner.UnitTick then
								owner.UnitTick(tick, unitID, unitDefID, hpRatio,
								               ux, uy, uz, unitCmds)
							end
						end
					end

					-- ---- Decision trace publish (see TRACE_INTERVAL) ----
					traceTicks[teamID] = (traceTicks[teamID] or 0) + 1
					if SimpleUnderAttack[teamID] then
						traceAttacked[teamID] = (traceAttacked[teamID] or 0) + 1
					end
					if n - (traceLast[teamID] or 0) >= TRACE_INTERVAL then
						local tally = ctx.trace[teamID]
						local nk = 0
						for key in pairs(tally) do nk = nk + 1; traceKeys[nk] = key end
						for k = nk + 1, #traceKeys do traceKeys[k] = nil end
						table.sort(traceKeys)
						for k = 1, nk do
							local key = traceKeys[k]
							traceKeys[k] = key .. ":" .. tally[key]
							tally[key] = nil
						end
						local traceLine = string.format(
							"f=%d;ai=%s;tech=%d;m=%d/%d+%.1f;e=%d/%d+%.0f;ms=%.2f;es=%.2f;paused=%d;rec=%d;nocomm=%d;ua=%d/%d;fac=%d;con=%d;mex=%d;tur=%d;army=%d;r=%s",
							n, luaAI or "?", TeamTechLevel[teamID] or 1, mcurrent, mstorage, mincome, ecurrent, estorage, eincome,
							mStall, eStall, ctx.stall.paused[teamID] or 0,
							ctx.reclaim.near[teamID] or 0,
							ctx.comm.lost[teamID] and 1 or 0,
							traceAttacked[teamID] or 0, traceTicks[teamID] or 0,
							SimpleFactoriesCount[teamID] or 0, SimpleConstructorCount[teamID] or 0,
							SimpleT1Mexes[teamID] or 0, SimpleTurretCount[teamID] or 0,
							SimpleArmyCount[teamID] or 0,
							table.concat(traceKeys, ","))
						if GG.Recorder and GG.Recorder.Log then
							GG.Recorder.Log(teamID, "simpleai", traceLine)
						end
						if TRACE_ECHO then Spring.Echo("[SimpleAI] team " .. teamID .. " " .. traceLine) end
						Spring.SetTeamRulesParam(teamID, "simpleai_trace", traceLine, { private = true })
						traceLast[teamID], traceAttacked[teamID], traceTicks[teamID] = n, 0, 0
					end

					SimpleUnderAttack[teamID] = false

				end
			end
		end -- n%15
	end

	-- ============================================================
	-- COUNTER BOOKKEEPING: built or given in, destroyed or taken out.
	-- ============================================================
	local commUnits = {}
	local function RegisterUnit(unitID, unitDefID, unitTeam)
		if IsCommander[unitDefID] and TeamFaction[unitTeam] == nil then
			TeamFaction[unitTeam] = FactionOf(UnitDefs[unitDefID]) or "arm"
			PopulateBuildLists(unitTeam, TeamFaction[unitTeam])
		end
		if IsCommander[unitDefID] then
			local set = commUnits[unitTeam]
			if not set then set = {}; commUnits[unitTeam] = set end
			set[unitID] = true
			TeamCommID[unitTeam] = unitID
			-- HOME is where the team's first commander appeared.
			if not ctx.home[unitTeam] then
				local hx, _, hz = Spring.GetUnitPosition(unitID)
				if hx then ctx.home[unitTeam] = { x = hx, z = hz } end
			end
		end

		if IsFactory[unitDefID] then
			if TRACE_ECHO then Spring.Echo(("[SimpleAI] team %d factory nanoframe %s (frame %d)"):format(unitTeam, UnitDefs[unitDefID].name, Spring.GetGameFrame())) end
			SimpleFactoriesCount[unitTeam] = SimpleFactoriesCount[unitTeam] + 1
			SimpleFactories[unitTeam][unitDefID] =
			(SimpleFactories[unitTeam][unitDefID] or 0) + 1
			if IsAirFactory[unitDefID] then
				ctx.counters.airFactories[unitTeam] = (ctx.counters.airFactories[unitTeam] or 0) + 1
			elseif IsSeaFactory[unitDefID] then
				ctx.counters.seaFactories[unitTeam] = (ctx.counters.seaFactories[unitTeam] or 0) + 1
			else
				SimpleLandFacCount[unitTeam] = (SimpleLandFacCount[unitTeam] or 0) + 1
			end
		end
		if IsExtractor[unitDefID] then
			SimpleT1Mexes[unitTeam] = SimpleT1Mexes[unitTeam] + 1
		end
		if IsConstructor[unitDefID] then
			SimpleConstructorCount[unitTeam] = SimpleConstructorCount[unitTeam] + 1
		end
		if IsCombat[unitDefID] then
			SimpleArmyCount[unitTeam] = (SimpleArmyCount[unitTeam] or 0) + 1
		end
		if IsConverter[unitDefID] then
			SimpleConverterCount[unitTeam] = (SimpleConverterCount[unitTeam] or 0) + 1
		end
		if IsTurret[unitDefID] then
			SimpleTurretCount[unitTeam] = (SimpleTurretCount[unitTeam] or 0) + 1
			if IsAATurret[unitDefID] then
				SimpleAATurretCount[unitTeam] = (SimpleAATurretCount[unitTeam] or 0) + 1
			end
		end
		-- a builder is created (nanoframe) now, but can only build once finished
	end

	-- Tech follows FINISHED builders.
	local function TechIn(unitDefID, unitTeam)
		local bt = ctx.BuilderTier[unitDefID] or 0
		if bt > 0 and TierBuilders[unitTeam] then
			TierBuilders[unitTeam][bt] = (TierBuilders[unitTeam][bt] or 0) + 1
			RecomputeTech(unitTeam)
		end
	end
	local function TechOut(unitDefID, unitTeam)
		local bt = ctx.BuilderTier[unitDefID] or 0
		if bt > 0 and TierBuilders[unitTeam] then
			TierBuilders[unitTeam][bt] = math.max(0, (TierBuilders[unitTeam][bt] or 1) - 1)
			RecomputeTech(unitTeam)
		end
	end
	local finished = {}   -- [unitID] = true once UnitFinished counted its tech

	function gadget:UnitCreated(unitID, unitDefID, unitTeam, builderID)
		if IsAITeamID[unitTeam] then
			RegisterUnit(unitID, unitDefID, unitTeam)
		end
	end

	function gadget:UnitFinished(unitID, unitDefID, unitTeam)
		if not TeamBuildLists[unitTeam] then return end
		if not finished[unitID] then
			finished[unitID] = true
			TechIn(unitDefID, unitTeam)
		end
		for i = 1, #behaviors do
			local b = behaviors[i]
			if b.UnitFinished then b.UnitFinished(unitID, unitDefID, unitTeam) end
		end
	end

	local function UnregisterUnit(unitID, unitDefID, unitTeam)
		if IsFactory[unitDefID] then
			SimpleFactoriesCount[unitTeam] =
			math.max(0, SimpleFactoriesCount[unitTeam] - 1)
			SimpleFactories[unitTeam][unitDefID] =
			math.max(0, (SimpleFactories[unitTeam][unitDefID] or 1) - 1)
			if IsAirFactory[unitDefID] then
				ctx.counters.airFactories[unitTeam] = math.max(0, (ctx.counters.airFactories[unitTeam] or 1) - 1)
			elseif IsSeaFactory[unitDefID] then
				ctx.counters.seaFactories[unitTeam] = math.max(0, (ctx.counters.seaFactories[unitTeam] or 1) - 1)
			else
				SimpleLandFacCount[unitTeam] =
				math.max(0, (SimpleLandFacCount[unitTeam] or 1) - 1)
			end
		end
		if IsExtractor[unitDefID] then
			SimpleT1Mexes[unitTeam] = math.max(0, SimpleT1Mexes[unitTeam] - 1)
		end
		if IsConstructor[unitDefID] then
			SimpleConstructorCount[unitTeam] =
			math.max(0, SimpleConstructorCount[unitTeam] - 1)
		end
		if IsCombat[unitDefID] then
			SimpleArmyCount[unitTeam] =
			math.max(0, (SimpleArmyCount[unitTeam] or 1) - 1)
		end
		if IsConverter[unitDefID] then
			SimpleConverterCount[unitTeam] =
			math.max(0, (SimpleConverterCount[unitTeam] or 1) - 1)
		end
		if IsTurret[unitDefID] then
			SimpleTurretCount[unitTeam] =
			math.max(0, (SimpleTurretCount[unitTeam] or 1) - 1)
			if IsAATurret[unitDefID] then
				SimpleAATurretCount[unitTeam] =
				math.max(0, (SimpleAATurretCount[unitTeam] or 1) - 1)
			end
		end
		if finished[unitID] then
			finished[unitID] = nil
			TechOut(unitDefID, unitTeam)
		end
		if IsCommander[unitDefID] then
			local set = commUnits[unitTeam]
			if set then set[unitID] = nil end
			if TeamCommID[unitTeam] == unitID then
				local other
				if set then
					for id in pairs(set) do
						if not other or id < other then other = id end
					end
				end
				TeamCommID[unitTeam] = other
				SimpleCommRetreating[unitTeam] = false
				SimpleCommRetreatPos[unitTeam] = nil
			end
		end
	end

	function gadget:UnitDestroyed(unitID, unitDefID, unitTeam,
	                              attackerID, attackerDefID, attackerTeam)
		SimpleRetreatState[unitID] = nil
		if IsAITeamID[unitTeam] then
			UnregisterUnit(unitID, unitDefID, unitTeam)
			for i = 1, #behaviors do
				local b = behaviors[i]
				if b.UnitLost then b.UnitLost(unitTeam, unitID, unitDefID) end
			end
		else
			finished[unitID] = nil
		end
		if attackerTeam and IsAITeamID[attackerTeam]
				and attackerTeam ~= unitTeam
				and unitTeam ~= gaiaTeamID
				and not Spring.AreTeamsAllied(attackerTeam, unitTeam) then
			for i = 1, #behaviors do
				local b = behaviors[i]
				if b.UnitKilled then b.UnitKilled(attackerTeam, unitID, unitDefID) end
			end
		end
	end

	function gadget:UnitGiven(unitID, unitDefID, unitTeam, oldTeam)
		if IsAITeamID[unitTeam] then
			RegisterUnit(unitID, unitDefID, unitTeam)
			local _, _, _, _, bp = Spring.GetUnitHealth(unitID)
			if (bp or 1) >= 1 and not finished[unitID] then
				finished[unitID] = true
				TechIn(unitDefID, unitTeam)
			end
			for i = 1, #behaviors do
				local b = behaviors[i]
				if b.UnitFinished then b.UnitFinished(unitID, unitDefID, unitTeam) end
			end
		end
	end

	function gadget:UnitTaken(unitID, unitDefID, unitTeam, newTeam)
		if IsAITeamID[unitTeam] then
			UnregisterUnit(unitID, unitDefID, unitTeam)
			SimpleRetreatState[unitID] = nil
		end
	end

	function gadget:UnitDamaged(unitID, unitDefID, damage, direction,
	                            attackerID, attackerDefID, attackerTeam, isParalyzer)
		if not unitDefID then return end
		local teamID = Spring.GetUnitTeam(unitID)
		if not IsAITeamID[teamID] then return end

		if not attackerTeam
				or attackerTeam == teamID
				or attackerTeam == gaiaTeamID
				or Spring.AreTeamsAllied(teamID, attackerTeam) then
			return
		end

		if attackerDefID and IsAir[attackerDefID] then
			SimpleAirThreat[teamID] = Spring.GetGameFrame()
		end

		if UnitDefs[unitDefID] and UnitDefs[unitDefID].isBuilding then
			SimpleUnderAttack[teamID] = true
			local nowF = Spring.GetGameFrame()
			for i = 1, #behaviors do
				local b = behaviors[i]
				if b.BaseDamaged then b.BaseDamaged(teamID, nowF) end
			end
		end
	end

end -- IsSyncedCode
