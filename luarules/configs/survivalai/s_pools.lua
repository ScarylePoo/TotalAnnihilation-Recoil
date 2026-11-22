--------------------------------------------------------------------------------
--
--  file:    s_pools.lua  (Survival AI module)
--  brief:   Builds the wave unit pools from factory build lists. Every unit a
--           factory can produce is a candidate; builders, factories, buildings
--           and unarmed units are excluded. Role comes from the unit's
--           buildmenucategory customparam, faction from factionname, tier from
--           the requiretech customparam (unit's own, else its factory's).
--
--           Pure module: takes a UnitDefs-shaped table, touches no engine
--           state, so it can be smoke-tested under plain lua5.1.
--
--------------------------------------------------------------------------------

local M = {}

-- requiretech values are strings like "tech2" / "2" / "T2"; pull the digit.
-- No param (or no digit) means tier 1.
local function TechToTier(v)
	if v == nil then return nil end
	local n = tonumber(string.match(tostring(v), "%d+"))
	return n
end

--------------------------------------------------------------------------------
-- Role classification. The tactical vocabulary lives in the `unitrole`
-- customparam ("Main Battle Tank - Tech 2", "Indirect Fire Support", ...);
-- buildmenucategory is only the build-menu grouping and is used as fallback.
-- Precedence matters: "Direct/Indirect Fire Support" must classify as
-- artillery before the generic "support" pattern can swallow it.
--------------------------------------------------------------------------------

-- TA:Recoil: a unit's role is the middle of its radar icon type
-- (gamedata/unit_icons.lua, e.g. "kbot_light_t1" -> light), which is where
-- every unit's role is already written down; aircraft get their own classes.
--   ground  scout, light, assault, heavy, artillery, rocket, aa, sniper, emp,
--           kamikaze, other
--   air     fighter (air_aa), gunship (air_assault), bomber (air_bomber,
--           air_torpedo), transport, scout
-- [unit name] = icon type, straight from gamedata/unit_icons.lua (UnitDefs in
-- LuaRules does not carry the icon type); nil under a plain-Lua smoke test.
local ICONS = (VFS and VFS.FileExists and VFS.FileExists("gamedata/unit_icons.lua"))
		and VFS.Include("gamedata/unit_icons.lua") or {}
local function IconOf(ud)
	return string.lower((ud and (ICONS[ud.name] or ud.iconType)) or "")
end

local function Classify(cp, ud)
	local icon = IconOf(ud)
	local family, role = string.match(icon, "^(%a+)_(%a+)")
	if not role then return "other" end
	-- nothing that needs water (the waves are land waves), and nothing whose
	-- job a wave has no use for: these come back as "transport", which
	-- M.Build leaves out of the pools
	if family == "ship" or family == "sub" then return "transport" end
	if role == "transport" or role == "torpedo" or role == "antinuke" or role == "radar"
			or role == "sonar" or role == "jammer" or role == "spy" or role == "builder" then
		return "transport"
	end
	if family == "air" or family == "seaplane" then
		if role == "aa" then return "fighter" end
		if role == "assault" then return "gunship" end
		if role == "bomber" then return "bomber" end
		if role == "scout" then return "scout" end
		return "other"
	end
	return role
end

-- Tier from the icon type's last part ("_t2", "_t3_x17"); 1 without one.
local function IconTier(ud)
	local n = string.match(IconOf(ud), "_t(%d)")
	return tonumber(n)
end

M.Classify = Classify

local function IsEligible(ud)
	if not ud then return false end
	if ud.isFactory then return false end           -- factories build, they don't march
	if ud.isBuilder then return false end           -- engineers / constructors
	local cp = ud.customParams or {}
	if cp.unittype == "building" then return false end
	if cp.iscommander or string.find(ud.name or "", "commander", 1, true) then return false end   -- (and its decoy)
	if not ud.canMove then return false end
	if (ud.weapons == nil) or (#ud.weapons == 0) then return false end
	if (ud.minWaterDepth or 0) > 0 then return false end  -- sea units: no land waves (yet)
	if (ud.metalCost or 0) <= 0 then return false end
	return true
end

--------------------------------------------------------------------------------
-- M.Build(unitDefs, unitDefNames) -> pools
--
-- pools = {
--   entries  = { {name, defID, cost, role, faction, tier, isAir}, ... },
--   byRole   = { [role]   = { entryIdx, ... } },
--   byTier   = { [tier]   = { entryIdx, ... } },
--   minCost  = cheapest entry cost,
--   maxTier  = highest tier seen,
-- }
--------------------------------------------------------------------------------

function M.Build(unitDefs, unitDefNames)
	local pools = {
		entries  = {},
		byRole   = {},
		byClass  = {},
		byTier   = {},
		factions = {},
		minCost  = math.huge,
		maxTier  = 1,
	}
	local seen        = {}   -- defID -> true (a unit can appear in several factories)
	local factionSeen = {}

	for facID = 1, #unitDefs do
		local fac = unitDefs[facID]
		if fac and fac.isFactory and fac.buildOptions then
			local facTier = TechToTier((fac.customParams or {}).requiretech) or 1
			for i = 1, #fac.buildOptions do
				local udid = fac.buildOptions[i]
				local ud   = unitDefs[udid]
				if ud and not seen[udid] and IsEligible(ud) then
					local cp    = ud.customParams or {}
					local class = Classify(cp, ud)
					-- Transports have no cargo logic in waves yet; leave them out
					if class ~= "transport" then
						seen[udid] = true
						local entry = {
							name    = ud.name,
							defID   = udid,
							cost    = ud.metalCost,
							role    = class,
							class   = class,
							faction = string.upper(string.match(ud.name or "", "^(%a+)_") or "Unknown"),   -- ARM / CORE
							tier    = IconTier(ud) or TechToTier(cp.requiretech) or facTier,
							isAir   = ud.canFly or false,
							-- Drop-wave data: what this can carry / whether it can ride
							cap      = ud.transportCapacity or 0,
							tmass    = ud.transportMass or math.huge,
							mass     = ud.mass or ud.metalCost or 100,
							portable = (not ud.canFly) and (not ud.cantBeTransported) or false,
						}
						local n = #pools.entries + 1
						pools.entries[n] = entry

						local r = pools.byRole[entry.role]
						if not r then r = {} ; pools.byRole[entry.role] = r end
						r[#r + 1] = n

						local c = pools.byClass[entry.class]
						if not c then c = {} ; pools.byClass[entry.class] = c end
						c[#c + 1] = n

						local t = pools.byTier[entry.tier]
						if not t then t = {} ; pools.byTier[entry.tier] = t end
						t[#t + 1] = n

						if entry.faction ~= "Unknown" and not factionSeen[entry.faction] then
							factionSeen[entry.faction] = true
							pools.factions[#pools.factions + 1] = entry.faction
						end

						if entry.cost < pools.minCost then pools.minCost = entry.cost end
						if entry.tier > pools.maxTier then pools.maxTier = entry.tier end
					end
				end
			end
		end
	end

	table.sort(pools.factions)   -- deterministic order for synced random picks
	return pools
end

-- Debug helper: one echo line per class bucket.
function M.Describe(pools, echo)
	echo = echo or print
	echo(string.format("[Survival] Pool: %d units, tiers 1-%d, cheapest %d metal, %d faction(s)",
		#pools.entries, pools.maxTier,
		pools.minCost ~= math.huge and pools.minCost or 0, #pools.factions))
	for class, list in pairs(pools.byClass) do
		echo(string.format("[Survival]   class %-10s x%d", class, #list))
	end
end

return M
