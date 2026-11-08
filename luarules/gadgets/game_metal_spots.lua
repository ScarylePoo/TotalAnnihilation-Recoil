function gadget:GetInfo()
	return {
		name    = "Metal Spots",
		desc    = "Finds the map's metal spots, masks them so only mexes build there, publishes them and their value",
		author  = "Scary le Poo (from Splinter Faction's map-defined metal spot finder and spot generator)",
		date    = "2026-11-08",
		license = "GNU GPL, v2 or later",
		layer   = -100,   -- before the output and upgrade gadgets
		enabled = true,
	}
end

--------------------------------------------------------------------------------
-- TA:Recoil mexes are metal makers on fixed spots (no metal extraction):
--  * spots come from the map's metal map, as the map maker placed them (Splinter Faction's map-defined scan:
--    3x3 average metal >= METAL_THRESHOLD, centre moved to the richest 3x3 nearby, near-duplicates merged); none
--    are moved, dropped or randomised
--  * each spot gets building mask 4 over a moho-sized block (+1 square margin, as SF does: the engine's rounding of
--    build positions can otherwise leave a row off the mask). Mexes have buildingMask 4, so they can only be built on
--    spots, and nothing else can be built there (other units keep the default mask 1)
--  * output per spot ("metalSpot_value") = BASE_VALUE x sqrt(players / 2): 2 metal at 1v1, gently more in bigger
--    games (4 players 2.83, 8 players 4). game_metal_spot_output.lua applies it (moho x3)
-- Published like SF's, so SF's widgets and our own read the same thing:
--   GG.metalMakerSpots = { {x, y, z}, ... }
--   GameRulesParams metalSpot_count, metalSpot_<i>_x / _z, metalSpot_value, metalSpot_players
-- A map without metal spots simply has none (user decision): no mex income there.
--------------------------------------------------------------------------------

if not gadgetHandler:IsSyncedCode() then
	return
end

local METAL_THRESHOLD      = 0.10   -- average metal (0-1) over a 3x3 of map squares for a spot
local CLUSTER_RADIUS       = 6      -- map squares (96 elmos): candidates closer than this are one spot
local CENTER_SEARCH_RADIUS = 2      -- map squares: move the centre to the richest 3x3 within this
local FOOTPRINT            = 5      -- the largest mex (moho mine, 5x5); a 3x3 mex fits the same mask
local MASK                 = 4
local BASE_VALUE           = 2      -- metal per spot at 1v1

local GetMetalAmount = Spring.GetMetalAmount
local SetSquareBuildingMask = Spring.SetSquareBuildingMask

local function MetalAvg3x3(cx, cz)
	local sum = 0
	for dx = -1, 1 do
		for dz = -1, 1 do
			sum = sum + (GetMetalAmount(cx + dx, cz + dz) or 0)
		end
	end
	return sum / 9
end

local function FindSpots()
	local sqX, sqZ = math.floor(Game.mapSizeX / 16), math.floor(Game.mapSizeZ / 16)
	local claimed, spots = {}, {}
	local r2 = CLUSTER_RADIUS * CLUSTER_RADIUS
	local function isClaimed(cx, cz)
		for i = 1, #claimed do
			local dx, dz = cx - claimed[i][1], cz - claimed[i][2]
			if dx * dx + dz * dz < r2 then
				return true
			end
		end
		return false
	end
	for x = 1, sqX - 2 do
		for z = 1, sqZ - 2 do
			local cx, cz = x + 1, z + 1
			if not isClaimed(cx, cz) and MetalAvg3x3(cx, cz) >= METAL_THRESHOLD then
				local bx, bz, best = cx, cz, MetalAvg3x3(cx, cz)
				for ox = -CENTER_SEARCH_RADIUS, CENTER_SEARCH_RADIUS do
					for oz = -CENTER_SEARCH_RADIUS, CENTER_SEARCH_RADIUS do
						local tx, tz = cx + ox, cz + oz
						if tx >= 1 and tx <= sqX - 2 and tz >= 1 and tz <= sqZ - 2 then
							local avg = MetalAvg3x3(tx, tz)
							if avg > best then
								bx, bz, best = tx, tz, avg
							end
						end
					end
				end
				-- a patch wider than CLUSTER_RADIUS is found from more than one edge, and each find moves to the same
				-- richest centre: compare final centres too, and claim both the find and its centre
				if not isClaimed(bx, bz) then
					spots[#spots + 1] = { sx = bx, sz = bz }
				end
				claimed[#claimed + 1] = { cx, cz }
				claimed[#claimed + 1] = { bx, bz }
			end
		end
	end
	return spots, sqX, sqZ
end

local function MaskSpot(sx, sz, sqX, sqZ)
	local radius = math.floor(FOOTPRINT / 2) + 1
	for dx = -radius, radius do
		for dz = -radius, radius do
			local mx, mz = sx + dx, sz + dz
			if mx >= 0 and mx < sqX and mz >= 0 and mz < sqZ then
				SetSquareBuildingMask(mx, mz, MASK)
			end
		end
	end
end

local function Players()
	local n = 0
	local gaia = Spring.GetGaiaTeamID()
	for _, teamID in ipairs(Spring.GetTeamList()) do
		if teamID ~= gaia then
			n = n + 1
		end
	end
	return math.max(n, 1)
end

function gadget:Initialize()
	local spots, sqX, sqZ = FindSpots()
	local published = {}
	for i, s in ipairs(spots) do
		MaskSpot(s.sx, s.sz, sqX, sqZ)
		local x, z = s.sx * 16, s.sz * 16
		published[i] = { x = x, y = Spring.GetGroundHeight(x, z), z = z }
		Spring.SetGameRulesParam("metalSpot_" .. i .. "_x", x)
		Spring.SetGameRulesParam("metalSpot_" .. i .. "_z", z)
	end
	Spring.SetGameRulesParam("metalSpot_count", #published)
	GG.metalMakerSpots = published

	local players = Players()
	local value = BASE_VALUE * math.sqrt(players / 2)
	Spring.SetGameRulesParam("metalSpot_players", players)
	Spring.SetGameRulesParam("metalSpot_value", value)
	Spring.Echo(string.format("[Metal Spots] %d spots, %d players: %.2f metal per spot", #published, players, value))
end
