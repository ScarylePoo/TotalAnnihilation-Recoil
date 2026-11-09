--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--
--  file:    luarules/configs/simpleai/behaviors/b_strategic.lua
--  brief:   Strategic weapons for the SimpleAI gadget (TA:Recoil): nuclear
--           missile silos and anti-nuke defences.
--
--             WANT      Every STRAT_CHECK frames the behavior decides what the
--                       team should have: an anti-nuke as soon as an enemy
--                       silo has been seen (finished or not) and the team has
--                       none; one silo once it is at tech 2, the game is
--                       SILO_MIN_FRAME old, its income carries the missiles
--                       and it is not stalling. b_construction's rung "ST"
--                       builds whatever services.StrategicWant(teamID) names.
--             STOCKPILE Silos and anti-nukes are told to stockpile while the
--                       energy bank is healthy: anti-nukes toward ANTI_STOCK,
--                       silos toward SILO_STOCK (unit_stockpile_limit caps
--                       them anyway).
--             FIRE      A silo with a missile ready fires at the most valuable
--                       cluster of enemy structures that is not covered by a
--                       loaded enemy anti-nuke, one shot per FIRE_SPACING.
--
--           Owns no units (TeamTick only). Reads ctx.IsSilo / IsAntiNuke,
--           ctx.techLevel, ctx.stall, tick resources.
--
--  license: GNU GPL, v2 or later
--
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

return function(ctx, lib, cfg, services)

	local STRAT_CHECK    = 600     -- frames between want decisions (~20s)
	local SILO_MIN_FRAME = 27000   -- no silo before this (15 min)
	local SILO_TECH      = 2
	local SILO_M_INCOME  = 18      -- metal income the team needs for a silo...
	local SILO_E_INCOME  = 1200    -- ...and energy income (a nuke costs ~50,000 E)
	local SILO_STOCK     = 2       -- missiles kept ready
	local ANTI_STOCK     = 3
	local STOCK_E_FRAC   = 0.35    -- stockpile only with this much of the energy bank
	local FIRE_SPACING   = 900     -- frames between launches per team (~30s)
	local NUKE_R         = 320     -- what a nuke flattens (radius, elmos)
	local ANTI_COVER     = 2000    -- an enemy anti-nuke protects this far (coverageRange)

	local IsSilo     = ctx.IsSilo or {}
	local IsAntiNuke = ctx.IsAntiNuke or {}
	local gaia       = cfg.gaiaTeamID
	local trace      = ctx.trace or {}

	local want       = {}   -- [teamID] = defID or false
	local lastCheck  = {}   -- [teamID] = frame
	local lastFire   = {}   -- [teamID] = frame
	local enemySilo  = {}   -- [teamID] = frame an enemy silo was last seen

	local function Count(teamID, key)
		local t = trace[teamID]
		if t then t[key] = (t[key] or 0) + 1 end
	end

	local valueOf = {}
	local function UnitValue(d)
		local v = valueOf[d]
		if not v then
			local ud = UnitDefs[d]
			v = (ud and ud.metalCost) or 0
			valueOf[d] = v
		end
		return v
	end

	-- The nuke silo def worth the most (its stockpile weapon's heaviest damage
	-- entry; the Neutron hurts only one side, the Silencer everything).
	local siloWorth = {}
	for d, ud in pairs(UnitDefs) do
		if IsSilo[d] then
			local best = 0
			for i = 1, #(ud.weapons or {}) do
				local wd = WeaponDefs[ud.weapons[i].weaponDef]
				if wd and wd.stockpile and wd.damages then
					for k = 0, #wd.damages do
						local v = wd.damages[k]
						if type(v) == "number" and v > best then best = v end
					end
				end
			end
			siloWorth[d] = best
		end
	end

	local function Decide(tick)
		local teamID = tick.teamID
		local n      = tick.frame
		local units  = tick.units
		local haveSilo, haveAnti = 0, 0
		for i = 1, #units do
			local d = Spring.GetUnitDefID(units[i])
			if d then
				if IsSilo[d] then haveSilo = haveSilo + 1 end
				if IsAntiNuke[d] then haveAnti = haveAnti + 1 end
			end
		end
		-- enemy silos anywhere (what we can see of them)
		local all = tick.allUnits
		for i = 1, #all do
			local uid = all[i]
			local ut  = Spring.GetUnitTeam(uid)
			if ut ~= teamID and ut ~= gaia and not Spring.AreTeamsAllied(teamID, ut) then
				local d = Spring.GetUnitDefID(uid)
				if d and IsSilo[d] then enemySilo[teamID] = n; break end
			end
		end

		local list = lib.GetBuildable(teamID, "strategic")
		local tech = (ctx.techLevel and ctx.techLevel[teamID]) or 1
		local stalling = ((ctx.stall and ctx.stall.v[teamID]) or 0) >= (cfg.STALL_ON or 0.2)

		if enemySilo[teamID] and haveAnti == 0 then
			for _, d in ipairs(list) do
				if IsAntiNuke[d] then want[teamID] = d; return end
			end
		end
		if haveSilo == 0 and tech >= SILO_TECH and n >= SILO_MIN_FRAME and not stalling
				and (tick.mInc or 0) >= SILO_M_INCOME and (tick.eInc or 0) >= SILO_E_INCOME then
			local best, bestW
			for _, d in ipairs(list) do
				if IsSilo[d] and (not best or (siloWorth[d] or 0) > bestW) then best, bestW = d, siloWorth[d] or 0 end
			end
			if best then want[teamID] = best; return end
		end
		want[teamID] = false
	end

	services.StrategicWant = function(teamID, frame)
		return want[teamID] or nil
	end

	-- The most valuable cluster of enemy structures not under a loaded enemy
	-- anti-nuke. Returns x, y, z or nil.
	local function NukeTarget(teamID, allUnits)
		local bld, anti = {}, {}
		for i = 1, #allUnits do
			local uid = allUnits[i]
			local ut  = Spring.GetUnitTeam(uid)
			if ut ~= teamID and ut ~= gaia and not Spring.AreTeamsAllied(teamID, ut) then
				local d  = Spring.GetUnitDefID(uid)
				local ud = d and UnitDefs[d]
				if ud and ud.isBuilding then
					local x, _, z = Spring.GetUnitPosition(uid)
					if x then
						bld[#bld + 1] = { x = x, z = z, v = UnitValue(d) }
						if IsAntiNuke[d] then
							local stock = Spring.GetUnitStockpile(uid)
							if (stock or 0) > 0 then anti[#anti + 1] = { x = x, z = z } end
						end
					end
				end
			end
		end
		if #bld == 0 then return nil end
		local r2, c2 = NUKE_R * NUKE_R, ANTI_COVER * ANTI_COVER
		local best, bestV
		for i = 1, #bld do
			local b = bld[i]
			local covered = false
			for k = 1, #anti do
				local dx, dz = anti[k].x - b.x, anti[k].z - b.z
				if dx * dx + dz * dz <= c2 then covered = true; break end
			end
			if not covered then
				local v = 0
				for k = 1, #bld do
					local dx, dz = bld[k].x - b.x, bld[k].z - b.z
					if dx * dx + dz * dz <= r2 then v = v + bld[k].v end
				end
				if not bestV or v > bestV then best, bestV = b, v end
			end
		end
		if not best then return nil end
		return best.x, Spring.GetGroundHeight(best.x, best.z), best.z
	end

	local B = { name = "strategic", order = 36 }

	function B.TeamInit(teamID)
		want[teamID], lastCheck[teamID], lastFire[teamID] = false, 0, 0
	end

	function B.TeamTick(tick)
		local teamID = tick.teamID
		local n      = tick.frame
		if (n - (lastCheck[teamID] or 0)) >= STRAT_CHECK then
			lastCheck[teamID] = n
			Decide(tick)
		end

		-- stockpile and fire
		local eOk = (tick.eCur or 0) > (tick.eStor or 1) * STOCK_E_FRAC
		local units = tick.units
		for i = 1, #units do
			local uid = units[i]
			local d   = Spring.GetUnitDefID(uid)
			if d and (IsSilo[d] or IsAntiNuke[d]) then
				local _, _, _, _, bp = Spring.GetUnitHealth(uid)
				if (bp or 1) >= 1 then
					local stock, queued = Spring.GetUnitStockpile(uid)
					stock, queued = stock or 0, queued or 0
					local goal = IsSilo[d] and SILO_STOCK or ANTI_STOCK
					if eOk and stock + queued < goal then
						Spring.GiveOrderToUnit(uid, CMD.STOCKPILE, {}, 0)
						Count(teamID, IsSilo[d] and "nuke.stock" or "anti.stock")
					end
					if IsSilo[d] and stock > 0 and (n - (lastFire[teamID] or 0)) >= FIRE_SPACING then
						local x, y, z = NukeTarget(teamID, tick.allUnits)
						if x then
							Spring.GiveOrderToUnit(uid, CMD.ATTACK, { x, y, z }, 0)
							lastFire[teamID] = n
							Count(teamID, "nuke.fire")
							if GG.Recorder and GG.Recorder.Log then
								GG.Recorder.Log(teamID, "strategic", ("nuke;x=%d;z=%d"):format(x, z))
							end
						end
					end
				end
			end
		end
	end

	return B
end
