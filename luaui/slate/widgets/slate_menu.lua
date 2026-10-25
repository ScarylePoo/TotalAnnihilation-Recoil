-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Menu",
		desc    = "Esc menu: settings, keybinds, widgets, share, graphs, log, pause, resign, quit",
		author  = "Scary le Poo",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = 1000, -- after the windows, so they see Esc first
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  Game menu.
--
--  A small MENU handle sits in the top right corner. Clicking it, or pressing
--  Esc, opens the menu: resume, the Slate windows (settings, keybinds,
--  widgets, share, economy graph, team statistics, log), the music row while
--  the music player runs, pause, and resign and quit, which both ask first.
--  Esc or a click outside the menu closes it. The menu does not pause the
--  game.
--
--  The windows belong to their own widgets; a window's button is left out of
--  the menu while its widget is not running. Those widgets get Esc first (to
--  close themselves), and Esc is left alone while a chat message is typed.
--
--  A game adds its own entries in slate_game.lua (menu = { {label=, command=,
--  confirm=, playersOnly=}, ... }); they come after the Slate windows.
--------------------------------------------------------------------------------

local DOCUMENT_PATH   = "menu.rml"
local UPDATE_INTERVAL = 0.25
local KEY_ESCAPE      = 27

-- must match #menu-button in menu.rml
local BUTTON_WIDTH  = 84
local BUTTON_HEIGHT = 30

local LAYOUT_NAME = "slate_menubutton"

local hud, S
local document
local view
local lastUpdate
local open = false
local confirming -- nil, or a key of CONFIRM

--------------------------------------------------------------------------------
-- what the buttons do
--------------------------------------------------------------------------------

local function OpenSettings()
	if WG.SlateOptions and WG.SlateOptions.toggle then
		WG.SlateOptions.toggle()
	end
end

-- Buttons that open another widget's window. available() says whether that
-- widget is running; the button is hidden while it is not.
local WINDOWS = {
	{id = "m-settings", available = function() return WG.SlateOptions and WG.SlateOptions.toggle end, action = OpenSettings},
	{id = "m-keybinds", available = function() return WG.SlateKeybinds and WG.SlateKeybinds.Toggle end,
		action = function() WG.SlateKeybinds.Toggle() end},
	{id = "m-widgets", available = function() return WG.SlateWidgetSelector and WG.SlateWidgetSelector.Toggle end,
		action = function() WG.SlateWidgetSelector.Toggle() end},
	{id = "m-share", available = function() return WG.SlateShare and WG.SlateShare.Toggle end,
		action = function() WG.SlateShare.Toggle() end},
	{id = "m-economy", available = function() return WG.SlateEconGraph and WG.SlateEconGraph.Toggle end,
		action = function() WG.SlateEconGraph.Toggle() end},
	{id = "m-graph", available = function() return WG.SlateEndGraph and WG.SlateEndGraph.Toggle end,
		action = function() WG.SlateEndGraph.Toggle() end},
	{id = "m-log", available = function() return WG.SlateLog and WG.SlateLog.Toggle end,
		action = function() WG.SlateLog.Toggle() end},
}

-- Things that cannot be taken back ask first. The game's own confirmed
-- entries are added at start-up under the key "game<i>".
local CONFIRM = {
	resign = {text = "Resign and watch as a spectator?", yes = "Yes, resign", command = "spectator"},
	quit   = {text = "Quit the game?", yes = "Yes, quit", command = "quitforce"},
}

-- The game's entries from slate_game.lua, with the id of each one's row.
local gameEntries = {}

--------------------------------------------------------------------------------

local function Refresh()
	view.SetClass("menu", "hidden", not open)
	view.SetClass("backdrop", "hidden", not open)
	view.SetClass("main-items", "hidden", confirming ~= nil)
	view.SetClass("confirm-items", "hidden", confirming == nil)

	for _, window in ipairs(WINDOWS) do
		view.SetClass(window.id, "hidden", not window.available())
	end
	local spectating = Spring.GetSpectatingState()
	for _, entry in ipairs(gameEntries) do
		view.SetClass(entry.id, "hidden", entry.playersOnly and spectating)
	end
	-- a spectator has nothing to resign from
	view.SetClass("m-resign", "hidden", spectating)

	local _, _, paused = Spring.GetGameSpeed()
	view.SetText("m-pause", paused and "Unpause" or "Pause")

	-- the music row, while the player is running
	local music = WG.SlateMusic and WG.SlateMusic.GetStatus and WG.SlateMusic.GetStatus()
	view.SetClass("music", "hidden", not music)
	if music then
		local label = "Now playing"
		if music.paused then label = "Paused" elseif music.silent then label = "Silence" elseif not music.playing then label = "Music" end
		view.SetText("music-label", label)
		view.SetText("music-title", hud.Escape(music.title ~= "" and music.title or "-"))
		view.SetText("music-artist", hud.Escape(music.artist))
		view.SetText("m-music-pause", (music.playing and not music.paused) and "Pause" or "Play")
	end

	local confirm = confirming and CONFIRM[confirming]
	if confirm then
		view.SetText("confirm-text", hud.Escape(confirm.text))
		view.SetText("m-confirm-yes", hud.Escape(confirm.yes))
	end
end

local function SetOpen(state)
	open = state
	confirming = nil
	if open then
		pcall(function() document:PullToFront() end) -- above the other HUD panels
	end
	Refresh()
end

local function OnButton(id, handler)
	hud.OnClick(view, id, function()
		hud.Sound("click")
		handler()
	end)
	local element = view.Element(id)
	if element then
		element:AddEventListener("mouseover", function() hud.Sound("hover") end)
	end
end

-- The game's extra rows, generated into the markup before the resign group.
local function AddGameEntries()
	local parts = {}
	for i, item in ipairs(S.game.menu or {}) do
		if type(item) == "table" and item.label and item.command then
			local id = "m-game" .. i
			local entry = {id = id, command = item.command, playersOnly = item.playersOnly and true or false}
			if item.confirm then
				entry.confirmKey = "game" .. i
				CONFIRM[entry.confirmKey] = {text = item.label .. "?", yes = "Yes, " .. item.label:lower(), command = item.command}
			end
			gameEntries[#gameEntries + 1] = entry
			parts[#parts + 1] = string.format('<div id="%s" class="button quiet%s">%s</div>',
				id, (#parts == 0) and " group" or "", hud.Escape(item.label))
		end
	end
	if #parts > 0 then
		view.Element("game-items").inner_rml = table.concat(parts)
		view.Forget()
	end
	for _, entry in ipairs(gameEntries) do
		OnButton(entry.id, function()
			if entry.confirmKey then
				confirming = entry.confirmKey
				Refresh()
			else
				SetOpen(false)
				Spring.SendCommands(entry.command)
			end
		end)
	end
end

--------------------------------------------------------------------------------
-- placement of the handle
--------------------------------------------------------------------------------

local function DefaultOrigin(vsx, vsy, w, h, scale)
	local margin = hud.Margin() * scale
	return vsx - w - margin, vsy - h - margin
end

local function Place()
	hud.PlacePanel(view.Element("menu-button"), LAYOUT_NAME, BUTTON_WIDTH, BUTTON_HEIGHT, DefaultOrigin)
end

--------------------------------------------------------------------------------

function widget:Initialize()
	S = WG.Slate
	if not S then
		widgetHandler:RemoveWidget()
		return
	end
	local helpers = include("slate/rml/core.lua")
	local result, reason = helpers.LoadDocument(DOCUMENT_PATH, widget)
	if not result then
		Spring.Echo("[Slate Menu] " .. tostring(reason))
		widgetHandler:RemoveWidget()
		return
	end
	hud = helpers
	hud.showInPregame = true -- a window the player opens; usable during faction choice and placement
	document = result

	view = hud.NewView(document)
	AddGameEntries() -- first: it replaces markup and forgets what the view assumed
	view.Assume("menu", "hidden", true)
	view.Assume("backdrop", "hidden", true)
	view.Assume("confirm-items", "hidden", true)
	view.Assume("main-items", "hidden", false)
	view.Assume("music", "hidden", true)

	OnButton("menu-button", function() SetOpen(not open) end)
	hud.OnClick(view, "backdrop", function() SetOpen(false) end)
	OnButton("m-resume", function() SetOpen(false) end)
	for _, window in ipairs(WINDOWS) do
		OnButton(window.id, function()
			SetOpen(false)
			if window.available() then
				window.action()
			end
		end)
	end
	OnButton("m-music-prev", function() if WG.SlateMusic then WG.SlateMusic.Previous() Refresh() end end)
	OnButton("m-music-pause", function() if WG.SlateMusic then WG.SlateMusic.TogglePause() Refresh() end end)
	OnButton("m-music-next", function() if WG.SlateMusic then WG.SlateMusic.Next() Refresh() end end)
	OnButton("m-pause", function()
		SetOpen(false)
		Spring.SendCommands("pause")
	end)
	OnButton("m-resign", function()
		confirming = "resign"
		Refresh()
	end)
	OnButton("m-quit", function()
		confirming = "quit"
		Refresh()
	end)
	OnButton("m-confirm-no", function()
		confirming = nil
		Refresh()
	end)
	OnButton("m-confirm-yes", function()
		local confirm = confirming and CONFIRM[confirming]
		SetOpen(false)
		if confirm then
			Spring.SendCommands(confirm.command)
		end
	end)

	hud.RegisterPanel(LAYOUT_NAME, "Menu", Place)
	hud.OnChange(LAYOUT_NAME, Place)
	Place()

	Refresh()
	hud.ShowPassive(document)
	lastUpdate = Spring.GetTimer()

	-- other widgets can open or close the menu
	WG.SlateMenu = {
		Toggle = function() SetOpen(not open) end,
		IsOpen = function() return open end,
	}
end

function widget:Shutdown()
	WG.SlateMenu = nil
	if hud then
		hud.UnregisterPanel(LAYOUT_NAME)
		hud.OffChange(LAYOUT_NAME)
	end
	if document then
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

function widget:KeyPress(key, mods, isRepeat)
	if not document or key ~= KEY_ESCAPE or isRepeat then
		return false
	end
	if Spring.IsUserWriting and Spring.IsUserWriting() then
		return false -- Esc cancels the chat message being typed
	end
	if Spring.IsGUIHidden() then
		return false
	end
	if confirming then
		confirming = nil
		Refresh()
	else
		SetOpen(not open)
	end
	return true
end

function widget:Update()
	if not document then
		return
	end
	if hud.FollowGuiHidden(document) then
		if open then
			SetOpen(false)
		end
		return
	end
	if not open then
		return
	end
	local now = Spring.GetTimer()
	if Spring.DiffTimers(now, lastUpdate) >= UPDATE_INTERVAL then
		lastUpdate = now
		Refresh()
	end
end
