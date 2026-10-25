-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Replay Controls",
		desc    = "Pause and speed buttons while watching a replay",
		author  = "Scary le Poo",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = 3,   -- after the resource bar (1), which it sits under
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  Replay controls: a strip under the resource bar with a pause button and
--  the replay speeds. Before the replay's game has begun the first button
--  skips the wait. The widget removes itself when no replay is being watched.
--  It stays on screen while units are selected, and shows the speed the game
--  is actually running at.
--------------------------------------------------------------------------------

local DOCUMENT_PATH = "replay.rml"

-- must match #replay in replay.rml
local PANEL_WIDTH  = 560
local PANEL_HEIGHT = 40
local RESOURCE_BAR_HEIGHT = 64 -- when the resource bar's own place is not known

local LAYOUT_NAME = "slate_replay"
local RESOURCE_BAR_LAYOUT = "slate_resourcebar"

local SPEEDS = {0.5, 1, 2, 3, 4, 5, 10, 20}

local UPDATE_INTERVAL = 0.2 -- seconds between looks at the game's speed

local hud, S
local document
local view

local wantedSpeed = nil -- a lower speed being stepped down to
local chosen = 2        -- index into SPEEDS of the last speed asked for
local lastUpdate

local function SpeedsRML()
	local parts = {}
	for i, speed in ipairs(SPEEDS) do
		parts[i] = string.format('<div id="rs%d" class="rb" data-speed="%d">%sx</div>', i, i, tostring(speed))
	end
	return table.concat(parts)
end

local function Refresh()
	local _, speed, paused = Spring.GetGameSpeed()
	local started = Spring.GetGameFrame() > 1
	view.SetText("replay-pause", (not started) and "Skip" or (paused and "Play" or "Pause"))
	view.SetClass("replay-pause", "active", started and paused)
	for i = 1, #SPEEDS do
		view.SetClass("rs" .. i, "active", i == chosen)
	end
	view.SetText("replay-now", string.format("%.1fx", speed or 1))
end

-- The engine only steps the speed. Up: raising the minimum speed jumps
-- there at once (and the minimum is then put back). Down: "slowdown" is sent
-- again and again from Update until the speed is low enough.
local function SetReplaySpeed(speed)
	local current = Spring.GetGameSpeed() -- the speed asked for (the second value is the speed reached)
	if speed > (current or 1) then
		wantedSpeed = nil
		Spring.SendCommands("setminspeed " .. speed)
		Spring.SendCommands("setminspeed " .. 0.1)
	else
		wantedSpeed = speed
	end
end

-- Just under the resource bar, wherever the player has put it; top centre
-- under where it would be when it is not running.
local function DefaultOrigin(vsx, vsy, w, h, scale)
	local layout = WG.SlateLayout
	local x1, y1, x2
	if layout and layout.GetRect then
		x1, y1, x2 = layout.GetRect(RESOURCE_BAR_LAYOUT)
	end
	if x1 then
		return (x1 + x2 - w) * 0.5, y1 - hud.Gap() * scale - h
	end
	return (vsx - w) * 0.5, vsy - (hud.Margin() + RESOURCE_BAR_HEIGHT + hud.Gap()) * scale - h
end

local function Place()
	hud.PlacePanel(view.Element("replay"), LAYOUT_NAME, PANEL_WIDTH, PANEL_HEIGHT, DefaultOrigin)
end

function widget:Initialize()
	S = WG.Slate
	if not S or not Spring.IsReplay() then
		widgetHandler:RemoveWidget(self)
		return
	end
	local helpers = include("slate/rml/core.lua")
	local result, reason = helpers.LoadDocument(DOCUMENT_PATH, widget)
	if not result then
		Spring.Echo("[Slate Replay Controls] " .. tostring(reason))
		widgetHandler:RemoveWidget(self)
		return
	end
	hud = helpers
	document = result
	view = hud.NewView(document)
	view.Element("replay-speeds").inner_rml = SpeedsRML()

	hud.OnClick(view, "replay-pause", function()
		hud.Sound("click")
		if Spring.GetGameFrame() > 1 then
			local _, _, paused = Spring.GetGameSpeed()
			Spring.SendCommands(paused and "pause 0" or "pause 1")
		else
			Spring.SendCommands("skip 1")
		end
		Refresh()
	end)
	view.Element("replay-speeds"):AddEventListener("mousedown", function(event)
		local i = hud.EventAttribute(event, "data-speed")
		if i and SPEEDS[i] and event.parameters and event.parameters.button == 0 then
			hud.Sound("click")
			chosen = i
			SetReplaySpeed(SPEEDS[i])
			Refresh()
		end
	end)

	hud.RegisterPanel(LAYOUT_NAME, "Replay Controls", Place)
	hud.OnChange(LAYOUT_NAME, Place)
	Place()
	hud.ShowPassive(document)
	lastUpdate = Spring.GetTimer()
	Refresh()
end

function widget:Shutdown()
	if hud then
		hud.UnregisterPanel(LAYOUT_NAME)
		hud.OffChange(LAYOUT_NAME)
		hud.CloseDocument(document)
		document = nil
	end
end

function widget:ViewResize()
	if hud and document then
		hud.UpdateScale()
		Place()
	end
end

function widget:Update()
	if not document then
		return
	end
	if wantedSpeed then
		local current = Spring.GetGameSpeed()
		if (current or 1) > wantedSpeed then
			Spring.SendCommands("slowdown")
		else
			wantedSpeed = nil
		end
	end
	if hud.FollowGuiHidden(document) then
		return
	end
	local now = Spring.GetTimer()
	if Spring.DiffTimers(now, lastUpdate) >= UPDATE_INTERVAL then
		lastUpdate = now
		Refresh()
	end
end
