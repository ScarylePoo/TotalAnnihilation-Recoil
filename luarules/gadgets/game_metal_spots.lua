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
--  * spots come from the map, as the map maker placed them: from mapconfig/map_metal_layout.lua when the map has
--    one (the "Lua metal map" many maps use: a list of {x, z, metal}; their own gadget writes it into the metal
--    map at a later layer than this one, so the metal map is still blank here), else from the metal map, one per
--    metal patch at the patch's metal-weighted centre (FindSpots); none are moved, dropped or randomised. A map
--    whose metal map is empty at Initialize is scanned again at GameStart, in case a gadget of its own fills it.
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

local METAL_THRESHOLD = 0.10   -- a map square counts as metal from this amount
local BLUR_RADIUS     = 3      -- map squares: box blur (twice) that turns each patch into one peak at its middle
local MIN_SEPARATION  = 5      -- map squares (80 elmos, a moho's width): closer peaks are one spot
local CENTRE_RADIUS   = 5      -- map squares: the weighted centre of the metal within this of a peak is the spot
local FOOTPRINT       = 5      -- the largest mex (moho mine, 5x5); a 3x3 mex fits the same mask
local MASK            = 4
local BASE_VALUE      = 2      -- metal per spot at 1v1

local LAYOUT_FILE     = "mapconfig/map_metal_layout.lua"

local GetMetalAmount = Spring.GetMetalAmount
local SetSquareBuildingMask = Spring.SetSquareBuildingMask

-- The map's own list of spots, when it ships one: mapconfig/map_metal_layout.lua returning { spots = { {x, z, metal},
-- ... } }. Each becomes a spot at its square; spots within MIN_SEPARATION of an earlier one are the same spot.
local function LayoutSpots()
	if not VFS.FileExists(LAYOUT_FILE) then return nil end
	local ok, cfg = pcall(VFS.Include, LAYOUT_FILE)
	local list = ok and type(cfg) == "table" and cfg.spots
	if type(list) ~= "table" or #list == 0 then return nil end
	local w, h = math.floor(Game.mapSizeX / 16), math.floor(Game.mapSizeZ / 16)
	local spots = {}
	local sep2 = MIN_SEPARATION * MIN_SEPARATION
	for _, s in ipairs(list) do
		local x, z = tonumber(s.x), tonumber(s.z)
		if x and z then
			local sx = math.max(0, math.min(w - 1, math.floor(x / 16)))
			local sz = math.max(0, math.min(h - 1, math.floor(z / 16)))
			local taken = false
			for _, o in ipairs(spots) do
				local dx, dz = o.sx - sx, o.sz - sz
				if dx * dx + dz * dz < sep2 then taken = true; break end
			end
			if not taken then
				spots[#spots + 1] = { sx = sx, sz = sz }
			end
		end
	end
	return spots, w, h
end

-- separable box blur of a flat grid (index x + z * w), clamped at the edges
local function BoxBlur(src, w, h, r)
	local tmp, out = {}, {}
	for z = 0, h - 1 do
		local row = z * w
		for x = 0, w - 1 do
			local sum = 0
			for dx = -r, r do
				local xx = math.min(w - 1, math.max(0, x + dx))
				sum = sum + src[row + xx]
			end
			tmp[row + x] = sum / (2 * r + 1)
		end
	end
	for z = 0, h - 1 do
		for x = 0, w - 1 do
			local sum = 0
			for dz = -r, r do
				local zz = math.min(h - 1, math.max(0, z + dz))
				sum = sum + tmp[zz * w + x]
			end
			out[z * w + x] = sum / (2 * r + 1)
		end
	end
	return out
end

-- Spots are the peaks of the blurred metal map (a patch of any size or shape blurs to one peak near its middle),
-- strongest first, merged within MIN_SEPARATION, then each moved to the metal-weighted centre of the patch around it
-- (a few mean-shift steps) and snapped to a square centre, where an odd-footprint building's centre lands.
local function FindSpots()
	local w, h = math.floor(Game.mapSizeX / 16), math.floor(Game.mapSizeZ / 16)
	local metal = {}
	for z = 0, h - 1 do
		for x = 0, w - 1 do
			local m = GetMetalAmount(x, z) or 0
			metal[z * w + x] = m >= METAL_THRESHOLD and m or 0
		end
	end
	local blur = BoxBlur(BoxBlur(metal, w, h, BLUR_RADIUS), w, h, BLUR_RADIUS)

	local peaks = {}
	local minPeak = METAL_THRESHOLD * 0.05
	for z = 1, h - 2 do
		for x = 1, w - 2 do
			local v = blur[z * w + x]
			if v > minPeak then
				local isMax = true
				for dz = -1, 1 do
					for dx = -1, 1 do
						local n = blur[(z + dz) * w + x + dx]
						-- ties (flat tops) go to the first square in scan order
						if n > v or (n == v and (dz < 0 or (dz == 0 and dx < 0))) then
							isMax = false
						end
					end
				end
				if isMax then
					peaks[#peaks + 1] = { x = x, z = z, v = v }
				end
			end
		end
	end
	table.sort(peaks, function(a, b) return a.v > b.v end)

	local spots = {}
	local sep2 = MIN_SEPARATION * MIN_SEPARATION
	local cr2 = CENTRE_RADIUS * CENTRE_RADIUS
	for _, p in ipairs(peaks) do
		-- weighted centre of the metal around the peak (squares are 0..1 wide; +0.5 = the square's middle)
		local cx, cz = p.x + 0.5, p.z + 0.5
		for _ = 1, 4 do
			local sw, sx, sz = 0, 0, 0
			local x0, z0 = math.floor(cx), math.floor(cz)
			for dz = -CENTRE_RADIUS, CENTRE_RADIUS do
				for dx = -CENTRE_RADIUS, CENTRE_RADIUS do
					local x, z = x0 + dx, z0 + dz
					if x >= 0 and x < w and z >= 0 and z < h and dx * dx + dz * dz <= cr2 then
						local m = metal[z * w + x]
						if m > 0 then
							sw, sx, sz = sw + m, sx + m * (x + 0.5), sz + m * (z + 0.5)
						end
					end
				end
			end
			if sw <= 0 then
				break
			end
			cx, cz = sx / sw, sz / sw
		end
		local fx, fz = math.floor(cx), math.floor(cz)
		local taken = false
		for _, s in ipairs(spots) do
			local dx, dz = s.sx - fx, s.sz - fz
			if dx * dx + dz * dz < sep2 then
				taken = true
				break
			end
		end
		if not taken then
			spots[#spots + 1] = { sx = fx, sz = fz }
		end
	end
	return spots, w, h
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

local function Publish(spots, sqX, sqZ, source)
	local published = {}
	for i, s in ipairs(spots) do
		MaskSpot(s.sx, s.sz, sqX, sqZ)
		local x, z = s.sx * 16 + 8, s.sz * 16 + 8   -- the square's centre
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
	Spring.Echo(string.format("[Metal Spots] %d spots (%s), %d players: %.2f metal per spot", #published, source, players, value))
	return #published
end

local found = 0

function gadget:Initialize()
	local spots, sqX, sqZ = LayoutSpots()
	local source = LAYOUT_FILE
	if not spots then
		spots, sqX, sqZ = FindSpots()
		source = "metal map"
	end
	found = Publish(spots, sqX, sqZ, source)
end

-- A map whose gadget fills the metal map after this one initialised: look again once everything has loaded.
function gadget:GameStart()
	if found == 0 then
		local spots, sqX, sqZ = FindSpots()
		found = Publish(spots, sqX, sqZ, "metal map at game start")
	end
end
