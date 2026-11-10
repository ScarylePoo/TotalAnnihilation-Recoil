function gadget:GetInfo()
	return {
		name    = "Geovent Spots",
		desc    = "Publishes the map's geothermal vents (GG.customGeoventSpots, customGeovent_* game rules params)",
		author  = "Scary le Poo (Splinter Faction's geovent spot format, without its random placement)",
		date    = "2026-11-08",
		license = "GNU GPL, v2 or later",
		layer   = -100,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
-- The map's own geovents, as placed by the map maker (features whose def is geoThermal), published the way
-- Splinter Faction's Geovent Spot Generator does, so its loader, minimap and yellow-column widgets work unchanged:
--   GG.customGeoventSpots = { {x, z}, ... }; customGeovent_count, customGeovent_<i>_x / _z
--------------------------------------------------------------------------------

if not gadgetHandler:IsSyncedCode() then
	return
end

local MERGE = 32   -- elmos: maps sometimes stack two vent features on one spot

local spots = {}

local function AddVent(x, z)
	for _, s in ipairs(spots) do
		if (s.x - x) ^ 2 + (s.z - z) ^ 2 < MERGE * MERGE then
			return false
		end
	end
	spots[#spots + 1] = { x = x, z = z }
	return true
end

-- a geothermal plant of this game, to test the vents with (any: they all need a vent under their yardmap's G squares)
local geoDefID
for udID, ud in pairs(UnitDefs) do
	if ud.needGeo then geoDefID = udID break end
end

local function Publish(when)
	GG.customGeoventSpots = spots
	local buildable = 0
	for i, s in ipairs(spots) do
		Spring.SetGameRulesParam("customGeovent_" .. i .. "_x", s.x)
		Spring.SetGameRulesParam("customGeovent_" .. i .. "_z", s.z)
		if geoDefID then
			local bx, by, bz = Spring.Pos2BuildPos(geoDefID, s.x, Spring.GetGroundHeight(s.x, s.z), s.z, 0)
			if (Spring.TestBuildOrder(geoDefID, bx, by, bz, 0) or 0) > 0 then buildable = buildable + 1 end
		end
	end
	Spring.SetGameRulesParam("customGeovent_count", #spots)
	Spring.Echo(string.format("[Geovent Spots] %d geovents (%s), %d take a geothermal plant", #spots, when, buildable))
end

local function Scan()
	for _, featureID in ipairs(Spring.GetAllFeatures()) do
		local fd = FeatureDefs[Spring.GetFeatureDefID(featureID)]
		if fd and fd.geoThermal then
			local x, _, z = Spring.GetFeaturePosition(featureID)
			AddVent(x, z)
		end
	end
end

function gadget:Initialize()
	-- the map's features from its SMF are there before gadgets initialise, and SF's widgets read the spots in their
	-- Initialize; a map that places its features from Lua (a feature placer gadget, often in LuaGaia, which loads
	-- after LuaRules) adds them through FeatureCreated below
	Scan()
	Publish("at load")
end

local pending = false

function gadget:FeatureCreated(featureID, allyTeamID)
	local fd = FeatureDefs[Spring.GetFeatureDefID(featureID)]
	if fd and fd.geoThermal then
		local x, _, z = Spring.GetFeaturePosition(featureID)
		if AddVent(x, z) then
			pending = true
		end
	end
end

-- vents placed since load are published once the game runs (all at once, not one param set per feature)
function gadget:GameStart()
	Scan()
	if pending then
		pending = false
		Publish("at game start")
	end
end

function gadget:GameFrame(n)
	if pending and n % 30 == 0 then
		pending = false
		Publish("frame " .. n)
	end
end
