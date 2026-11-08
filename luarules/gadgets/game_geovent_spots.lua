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

function gadget:Initialize()
	-- map features are loaded before gadgets initialise, and SF's widgets read the spots in their Initialize
	local spots = {}
	for _, featureID in ipairs(Spring.GetAllFeatures()) do
		local fd = FeatureDefs[Spring.GetFeatureDefID(featureID)]
		if fd and fd.geoThermal then
			local x, _, z = Spring.GetFeaturePosition(featureID)
			local dup = false
			for _, s in ipairs(spots) do
				if (s.x - x) ^ 2 + (s.z - z) ^ 2 < MERGE * MERGE then
					dup = true
					break
				end
			end
			if not dup then
				spots[#spots + 1] = { x = x, z = z }
			end
		end
	end
	GG.customGeoventSpots = spots
	for i, s in ipairs(spots) do
		Spring.SetGameRulesParam("customGeovent_" .. i .. "_x", s.x)
		Spring.SetGameRulesParam("customGeovent_" .. i .. "_z", s.z)
	end
	Spring.SetGameRulesParam("customGeovent_count", #spots)
	Spring.Echo("[Geovent Spots] " .. #spots .. " geovents")
end
