function widget:GetInfo()
	return {
		name    = "Metal Spot Rings",
		desc    = "F4 shows bright rings on the metal spots instead of the metal map; so does choosing a mex to build",
		author  = "Scary le Poo",
		date    = "2026-11-08",
		license = "GNU GPL, v2 or later",
		layer   = 5,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
-- TA:Recoil mexes only go on metal spots (luarules/gadgets/game_metal_spots.lua), so the engine's metal map view is
-- no use: whenever it switches on (F4, "showmetalmap"), this widget switches it straight back off and toggles its
-- rings instead. The rings also show, without F4, while a mex is the active build command (or a selected builder is
-- hovering a spot with right-click mex placement, game_metal_maker_placement_snapping.lua).
-- Free spots: a bright pulsing gold ring with a slowly turning dashed outer ring and a faint fill. Spots with a mex:
-- a dim ring in the owner's colour, so it is plain at a glance which spots are left.
--------------------------------------------------------------------------------

local INNER_R   = 38
local OUTER_R   = 54
local DASHES    = 12
local OCCUPIED  = 48

local spGetMapDrawMode  = Spring.GetMapDrawMode
local spGetActiveCommand = Spring.GetActiveCommand
local spGetUnitsInCylinder = Spring.GetUnitsInCylinder
local spGetUnitDefID    = Spring.GetUnitDefID
local spGetUnitTeam     = Spring.GetUnitTeam
local spGetTeamColor    = Spring.GetTeamColor
local spIsSphereInView  = Spring.IsSphereInView
local spGetGroundHeight = Spring.GetGroundHeight

local glColor, glVertex, glBeginEnd, glLineWidth = gl.Color, gl.Vertex, gl.BeginEnd, gl.LineWidth

local isMex = {}
for unitDefID, ud in pairs(UnitDefs) do
	if ud.customParams and ud.customParams.metal_extractor then
		isMex[unitDefID] = true
	end
end

local toggled = false
local occupiedTeam = {}   -- spot index -> teamID of a mex on it, refreshed twice a second
local refresh = 0

local function SpotY(s)
	return math.max(spGetGroundHeight(s.x, s.z), 0) + 2   -- on the water surface for underwater spots
end

local function Ring(x, y, z, r, segs, a0)
	for i = 0, segs do
		local a = a0 + i / segs * 2 * math.pi
		glVertex(x + math.cos(a) * r, y, z + math.sin(a) * r)
	end
end

local function Disc(x, y, z, r)
	glVertex(x, y, z)
	for i = 0, 32 do
		local a = i / 32 * 2 * math.pi
		glVertex(x + math.cos(a) * r, y, z + math.sin(a) * r)
	end
end

local function Dashes(x, y, z, r, a0)
	local step = 2 * math.pi / DASHES
	for i = 0, DASHES - 1 do
		local a1 = a0 + i * step
		local a2 = a1 + step * 0.55
		glVertex(x + math.cos(a1) * r, y, z + math.sin(a1) * r)
		glVertex(x + math.cos(a2) * r, y, z + math.sin(a2) * r)
	end
end

local function Wanted()
	if toggled then
		return true
	end
	local _, cmdID = spGetActiveCommand()
	return cmdID and cmdID < 0 and isMex[-cmdID] or false
end

function widget:Update(dt)
	-- F4: keep the engine's metal map off, toggle our rings instead
	if spGetMapDrawMode() == "metal" then
		Spring.SendCommands("showmetalmap")
		toggled = not toggled
	end
	refresh = refresh - dt
	if refresh <= 0 and WG.metalMakerSpots and Wanted() then
		refresh = 0.5
		occupiedTeam = {}
		for i, s in ipairs(WG.metalMakerSpots) do
			for _, u in ipairs(spGetUnitsInCylinder(s.x, s.z, OCCUPIED)) do
				if isMex[spGetUnitDefID(u)] then
					occupiedTeam[i] = spGetUnitTeam(u)
					break
				end
			end
		end
	end
end

function widget:DrawWorldPreUnit()
	local spots = WG.metalMakerSpots
	if not spots or Spring.IsGUIHidden() or not Wanted() then
		return
	end
	local t = Spring.GetGameSeconds() + Spring.GetFrameTimeOffset() / 30
	local pulse = 0.65 + 0.35 * math.sin(t * 4)
	local spin = t * 0.6
	gl.DepthTest(false)
	for i, s in ipairs(spots) do
		local y = SpotY(s)
		if spIsSphereInView(s.x, y, s.z, OUTER_R) then
			local team = occupiedTeam[i]
			if team then
				local r, g, b = spGetTeamColor(team)
				glLineWidth(2)
				glColor(r, g, b, 0.45)
				glBeginEnd(GL.LINE_STRIP, Ring, s.x, y, s.z, INNER_R, 32, 0)
			else
				glColor(1, 0.85, 0.2, 0.12 * pulse)
				glBeginEnd(GL.TRIANGLE_FAN, Disc, s.x, y, s.z, INNER_R)
				glLineWidth(8)
				glColor(1, 0.75, 0.1, 0.25 * pulse)   -- soft glow under the ring
				glBeginEnd(GL.LINE_STRIP, Ring, s.x, y, s.z, INNER_R, 40, 0)
				glLineWidth(3.5)
				glColor(1, 0.95, 0.4, pulse)
				glBeginEnd(GL.LINE_STRIP, Ring, s.x, y, s.z, INNER_R, 40, 0)
				glLineWidth(2)
				glColor(1, 0.85, 0.25, 0.7)
				glBeginEnd(GL.LINES, Dashes, s.x, y, s.z, OUTER_R, spin)
			end
		end
	end
	glLineWidth(1)
	glColor(1, 1, 1, 1)
	gl.DepthTest(true)
end
