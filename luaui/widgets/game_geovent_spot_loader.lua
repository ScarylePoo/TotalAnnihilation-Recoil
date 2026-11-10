-- From Splinter Faction (LuaUI/Widgets/game_geovent_spot_loader.lua).
function widget:GetInfo()
	return {
		name      = "Geovent Spot Loader",
		desc      = "Loads custom geovent positions from GameRulesParams into WG for widget use",
		author    = "",
		date      = "2025",
		license   = "GPLv2 or later",
		layer     = 0,
		enabled   = true,
	}
end

local GetGameRulesParam = Spring.GetGameRulesParam
local GetGroundHeight   = Spring.GetGroundHeight

local loadedCount = -1

local function Load()
	-- the same table on a reload: the minimap drawer caches it once it exists
	local geoSpots = WG.customGeoventSpots or {}
	for i = #geoSpots, 1, -1 do geoSpots[i] = nil end
	local count = GetGameRulesParam("customGeovent_count") or 0
	loadedCount = count

	for i = 1, count do
		local x = GetGameRulesParam("customGeovent_" .. i .. "_x")
		local z = GetGameRulesParam("customGeovent_" .. i .. "_z")
		if x and z then
			local y = GetGroundHeight(x, z)
			table.insert(geoSpots, {x = x, y = y, z = z})
		end
	end

	WG.customGeoventSpots = geoSpots
	Spring.Echo("[GeoventSpotLoader] Loaded " .. #geoSpots .. " custom geovent spots into WG.customGeoventSpots")
end

function widget:Initialize()
	Load()
end

-- a map that places its vents from Lua publishes them after load (game_geovent_spots.lua)
function widget:GameFrame(n)
	if n % 30 == 0 and (GetGameRulesParam("customGeovent_count") or 0) ~= loadedCount then
		Load()
	end
end

function widget:Shutdown()
	WG.customGeoventSpots = nil
end