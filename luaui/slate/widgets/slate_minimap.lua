--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--
--  Minimap placement and frame of the RmlUi HUD. Puts the engine's minimap in
--  the top left corner, sized to the map's proportions, and draws a Slate
--  frame around it. The minimap itself stays the engine's: it is drawn by the
--  engine before RmlUi and does not bend to the UI, so the frame is hollow and
--  follows the minimap's geometry every frame (wherever the engine has it).
--
--  The size follows the "Minimap size" setting (slate_minimapsize).
--
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

function widget:GetInfo()
	return {
		name    = "Slate Minimap",

		desc    = "Places the default minimap in the top-left corner with a frame around it ",
		author  = "Scary le Poo",
		date    = "2026-10-24",
		license = "GPL v2 or later",
		layer   = 1000,
		enabled = true,
	}
end

local DOCUMENT_PATH = "minimap.rml"

local MINIMAP_HEIGHT_RATIO = 400 / 1440 -- share of the screen's height; tuned at 1440p
local FRAME_DP = 8    -- the frame's thickness in dp (must match the borders in minimap.rml: 1 + 6 + 1)
local MARGIN = 4      -- pixels between the screen's edge and the frame
local SETTLE_FRAMES = 30 -- the engine may move the minimap again while loading; repeat for this long

local spSendCommands       = Spring.SendCommands
local spGetMiniMapGeometry = Spring.GetMiniMapGeometry

local hud, S
local document
local view
local frames = 0
local shown = "" -- the geometry the frame was last given

local function round(x)
	return math.floor(x + 0.5)
end

-- the frame's thickness in pixels at the current interface scale
local function FramePx()
	local scale = (hud and hud.GetScale()) or 1
	return math.max(2, round(FRAME_DP * scale))
end

local function SetMinimap()
	local vsx, vsy = Spring.GetViewGeometry()
	local aspect = Game.mapSizeZ / Game.mapSizeX
	local size = (S and S.Get("minimapSize")) or 1
	local h = round(vsy * MINIMAP_HEIGHT_RATIO * size)
	local w = round(h / aspect)
	-- a wide map gets a wide minimap, but never wider than a third of the screen
	if w > vsx / 3 then
		w = round(vsx / 3)
		h = round(w * aspect)
	end
	local inset = FramePx() + MARGIN
	spSendCommands("minimap geo " .. inset .. " " .. inset .. " " .. w .. " " .. h)
	spSendCommands("minimap border 0")
end

-- the glass band takes the theme's panel colour (opacity and tint settings)
local function TintFrame()
	if not (view and S and S.Colors) then return end
	local c = S.Colors()
	local a = math.max(c.opacity or 0.9, 0.6)
	view.Element("minimap-glass").style["border-color"] = string.format("rgba(%d,%d,%d,%d)",
		round(c.panel[1] * 255), round(c.panel[2] * 255), round(c.panel[3] * 255), round(a * 255))
end

-- a setting changed (minimap size, interface size, opacity, tint): size the minimap again and re-wrap it
local function OnSettings()
	frames = 0
	shown = ""
	SetMinimap()
	TintFrame()
end

-- wraps the frame around wherever the minimap is now
local function PlaceFrame()
	if not document then
		return
	end
	local x, y, w, h = spGetMiniMapGeometry() -- y from the bottom of the screen
	if not x or not w or w <= 0 or h <= 0 then
		return
	end
	local _, vsy = Spring.GetViewGeometry()
	local pad = FramePx()
	local key = x .. " " .. y .. " " .. w .. " " .. h .. " " .. vsy .. " " .. pad
	if key ~= shown then
		shown = key
		local element = view.Element("minimap-frame")
		element.style["left"] = (x - pad) .. "px"
		element.style["top"] = (vsy - (y + h) - pad) .. "px"
		element.style["width"] = (w + 2 * pad) .. "px"
		element.style["height"] = (h + 2 * pad) .. "px"
	end
end

function widget:Initialize()
	SetMinimap()
	local helpers = include("slate/rml/core.lua")
	local result, reason = helpers.LoadDocument(DOCUMENT_PATH, widget)
	if not result then
		Spring.Echo("[Slate Minimap] " .. tostring(reason))
		return -- the minimap is still placed, only without a frame
	end
	hud = helpers
	hud.showInPregame = true -- the minimap is used to pick a start spot
	document = result
	view = hud.NewView(document)
	S = hud.Slate()
	hud.OnChange("slate_minimap", OnSettings)
	TintFrame()
	PlaceFrame()
	hud.ShowPassive(document)
end

function widget:Shutdown()
	if hud then
		hud.OffChange("slate_minimap")
		hud.CloseDocument(document)
		document = nil
	end
end

function widget:ViewResize()
	SetMinimap()
	frames = 0
	if hud and document then
		hud.UpdateScale()
	end
end

function widget:Update()
	if frames < SETTLE_FRAMES then
		frames = frames + 1
		SetMinimap()
	end
	if document and not hud.FollowGuiHidden(document) then
		PlaceFrame() -- four numbers compared; the frame is touched only when they change
	end
end
