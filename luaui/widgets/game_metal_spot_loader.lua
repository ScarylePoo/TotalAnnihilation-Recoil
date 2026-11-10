-- From Splinter Faction (LuaUI/Widgets/game_metal_spot_loader.lua).
function widget:GetInfo()
	return {
		name    = "Metal Spot Loader",
		desc    = "Loads metal maker spots from GameRulesParams into WG",
		author  = "",
		date    = "2025-06-10",
		license = "GPLv2",
		layer   = 0,
		enabled = true,
	}
end

local GetGameRulesParam = Spring.GetGameRulesParam
local GetGroundHeight   = Spring.GetGroundHeight

local function Load()
	-- the same table on a reload: other widgets keep a reference to it (the minimap drawer caches it once it exists)
	local metalSpots = WG.metalMakerSpots or {}
	for i = #metalSpots, 1, -1 do metalSpots[i] = nil end
	local count = GetGameRulesParam("metalSpot_count") or 0

	for i = 1, count do
		local x = GetGameRulesParam("metalSpot_" .. i .. "_x")
		local z = GetGameRulesParam("metalSpot_" .. i .. "_z")
		if x and z then
			local y = GetGroundHeight(x, z)
			table.insert(metalSpots, {x = x, y = y, z = z})
		end
	end

	WG.metalMakerSpots = metalSpots
	Spring.Echo("[MetalSpotLoader] Loaded " .. #metalSpots .. " metal maker spots into WG.metalMakerSpots")
end

function widget:Initialize()
	Load()
end

-- the gadget publishes late on a map whose own gadget fills the metal map (game_metal_spots.lua, GameStart)
function widget:GameStart()
	if #(WG.metalMakerSpots or {}) == 0 then
		Load()
	end
end