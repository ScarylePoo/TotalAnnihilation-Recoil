function widget:GetInfo()
	return {
		name    = "Slate Name Tags",
		desc    = "The owner's name in a small Slate pill under every visible commander (and decoy commander)",
		author  = "Scary le Poo",
		date    = "2026-11-08",
		license = "GNU GPL, v2 or later",
		layer   = 900,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
-- Replaces Splinter Faction's World Labels commander tags in Slate's look: the pill is a .panel (glass, border,
-- the player's opacity and colour tint), with a dot in the team colour and the player's or AI's name.
-- Decoy commanders get their owner's tag too, exactly like the real one: a tag-less commander would give a
-- decoy away. Tags are pooled elements in one passive document (nametags.rml), moved every frame.
--------------------------------------------------------------------------------

local DOCUMENT_PATH = "nametags.rml"
local POOL_SIZE     = 32      -- most tags at once
local GAP_DP        = 6       -- between the unit's footprint and the tag
local SCAN_INTERVAL = 0.5     -- seconds between visibility rescans; positions update every frame

local spGetUnitViewPosition = Spring.GetUnitViewPosition
local spGetUnitTeam         = Spring.GetUnitTeam
local spGetUnitDefID        = Spring.GetUnitDefID
local spIsUnitVisible       = Spring.IsUnitVisible
local spWorldToScreenCoords = Spring.WorldToScreenCoords
local spGetTeamColor        = Spring.GetTeamColor
local spGetCameraVectors    = Spring.GetCameraVectors
local spGetUnitLosState     = Spring.GetUnitLosState
local spGetMyAllyTeamID     = Spring.GetMyAllyTeamID
local spGetSpectatingState  = Spring.GetSpectatingState

local hud, document, view
local tags = {}            -- pool: { element, nameElement, pipElement, unitID }
local isCommanderDef = {}
local radiusOfDef = {}
local commanders = {}      -- unitID -> true (every commander we know of)
local visible = {}         -- unitIDs on screen at the last scan
local scanTimer = SCAN_INTERVAL
local nameCache = {}       -- teamID -> name

for unitDefID, ud in pairs(UnitDefs) do
	if (ud.customParams and ud.customParams.iscommander) or ud.name:find("decoycommander") then
		isCommanderDef[unitDefID] = true
		radiusOfDef[unitDefID] = ud.radius or 20
	end
end

local function TeamName(teamID)
	if nameCache[teamID] then
		return nameCache[teamID]
	end
	local _, leader, _, isAI = Spring.GetTeamInfo(teamID, false)
	local name
	if isAI then
		local _, aiName, _, shortName = Spring.GetAIInfo(teamID)
		name = aiName or shortName or "AI"
	elseif leader then
		name = Spring.GetPlayerInfo(leader, false)
	end
	name = name or ("Team " .. teamID)
	nameCache[teamID] = name
	return name
end

local function Track(unitID, unitDefID)
	if isCommanderDef[unitDefID] then
		commanders[unitID] = true
	end
end

function widget:UnitCreated(unitID, unitDefID)        Track(unitID, unitDefID) end
function widget:UnitEnteredLos(unitID)                Track(unitID, spGetUnitDefID(unitID)) end
function widget:UnitDestroyed(unitID)                 commanders[unitID] = nil end
function widget:UnitGiven(unitID, unitDefID)          Track(unitID, unitDefID) end
function widget:PlayerChanged()                       nameCache = {} end
function widget:TeamChanged()                         nameCache = {} end

-- Only commanders in line of sight get a tag. IsUnitVisible also counts radar blips, and a radar blip's position is
-- deliberately off (radar error), so an enemy commander that left sight left its tag floating near it, and a cloaked
-- one kept its tag. Checked every frame: the scan only runs twice a second.
local function InSight(unitID)
	local _, fullView = spGetSpectatingState()
	if fullView then
		return true
	end
	local los = spGetUnitLosState(unitID, spGetMyAllyTeamID())   -- a table (raw bits need full read)
	return los and los.los
end

local function Rescan()
	visible = {}
	for unitID in pairs(commanders) do
		if not spGetUnitDefID(unitID) then
			commanders[unitID] = nil
		elseif spIsUnitVisible(unitID, 60, false) and InSight(unitID) then
			visible[#visible + 1] = unitID
		end
	end
end

local function Hide(tag)
	if tag.unitID then
		tag.unitID = nil
		tag.element:SetClass("hidden", true)
	end
end

function widget:Update(dt)
	if not document or hud.FollowGuiHidden(document) then
		return
	end
	scanTimer = scanTimer + dt
	if scanTimer >= SCAN_INTERVAL then
		scanTimer = 0
		Rescan()
	end
	local vsx, vsy = Spring.GetViewGeometry()
	local scale = hud.GetScale()
	local cam = spGetCameraVectors()
	local up = cam and cam.up or { 0, 1, 0 }
	local used = 0
	for _, unitID in ipairs(visible) do
		local x, y, z = spGetUnitViewPosition(unitID)
		local unitDefID = spGetUnitDefID(unitID)
		local teamID = spGetUnitTeam(unitID)
		if x and unitDefID and teamID and used < POOL_SIZE and InSight(unitID) then
			-- anchor just below the unit: its base, pushed down the screen by a third of its radius (in world units along
			-- the camera's up vector, so the gap stays right at any zoom and tilt)
			local r = (radiusOfDef[unitDefID] or 20) * 0.35   -- the view position is already the unit's base
			local sx, sy = spWorldToScreenCoords(x - up[1] * r, y - up[2] * r, z - up[3] * r)
			if sx and sx > -200 and sx < vsx + 200 and sy > -100 and sy < vsy + 100 then
				used = used + 1
				local tag = tags[used]
				if tag.unitID ~= unitID then
					tag.unitID = unitID
					tag.nameElement.inner_rml = hud.Escape(TeamName(teamID))
					local tr, tg, tb = spGetTeamColor(teamID)
					tag.pipElement.style["background-color"] = hud.Rgb(tr, tg, tb)
					tag.element:SetClass("hidden", false)
				end
				local w = tag.element.offset_width or 0
				tag.element.style["left"] = string.format("%dpx", math.floor(sx - w * 0.5))
				tag.element.style["top"] = string.format("%dpx", math.floor(vsy - sy + GAP_DP * scale))
			end
		end
	end
	for i = used + 1, POOL_SIZE do
		Hide(tags[i])
	end
end

function widget:Initialize()
	if not WG.Slate then
		widgetHandler:RemoveWidget(self)
		return
	end
	local helpers = include("slate/rml/core.lua")
	local result, reason = helpers.LoadDocument(DOCUMENT_PATH, widget)
	if not result then
		Spring.Echo("[Slate Name Tags] " .. tostring(reason))
		widgetHandler:RemoveWidget(self)
		return
	end
	hud = helpers
	hud.showInPregame = true
	document = result
	view = hud.NewView(document)
	local parts = {}
	for i = 1, POOL_SIZE do
		parts[#parts + 1] = string.format(
			'<div id="tag%d" class="tag panel hidden"><div id="pip%d" class="pip"></div><div id="name%d" class="name"></div></div>', i, i, i)
	end
	view.Element("tags").inner_rml = table.concat(parts)
	for i = 1, POOL_SIZE do
		tags[i] = {
			element = document:GetElementById("tag" .. i),
			pipElement = document:GetElementById("pip" .. i),
			nameElement = document:GetElementById("name" .. i),
		}
	end
	for _, unitID in ipairs(Spring.GetAllUnits()) do
		Track(unitID, spGetUnitDefID(unitID))
	end
	hud.ShowPassive(document)
end

function widget:Shutdown()
	if document and hud then
		hud.CloseDocument(document)
	end
	document = nil
end
