-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Faction Chooser",
		desc    = "Pregame faction choice; sends the choice to the game_spawn gadget",
		author  = "Scary le Poo; SplinterFaction Team",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = 2000, -- the placement widget keeps everything at 1800 and up running in pregame
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  The screen before the game proper, where each player picks a faction. The
--  screen is dimmed, with one card per faction and a countdown above them. A
--  click on a card is final. A player who has not chosen when the time runs
--  out gets a faction at random. Spectators see the dim, the heading and the
--  countdown only.
--
--  The countdown is driven by game frames, not the wall clock, so it respects
--  game speed and pause. The gadget broadcasts the real deadline (it is
--  shortened once everyone has chosen) and the current phase; the widget
--  removes itself when the phase is no longer "faction".
--
--  WHAT A GAME MUST PROVIDE
--
--  This widget is kept for games that have a faction choice; a game without
--  one need do nothing, the widget removes itself quietly. A game that wants
--  it provides:
--
--    a gadget (game_spawn.lua in the game it came from) that
--      - sets the game rules param "phase" to "faction" while the choice is
--        open and to anything else ("placement", "done") once it is over;
--      - sets "factionDeadlineFrame" to the game frame the choice closes at;
--      - listens in RecvLuaMsg for a message of SPAWN_MSG_BYTE followed by the
--        unitDefID of the chosen faction's commander, and spawns that;
--
--    the faction list, in slate_game.lua:
--      factions = {
--        { id = "<commander unit name>", name = "Faction", blurb = "A line or
--          two about it.", picture = "<image path>", color = "#rrggbb" },
--        ...
--      }
--      id is the unitDef name of the commander the gadget is to spawn; picture
--      is a file path from the game root (shown 392x220 dp, premultiplied
--      alpha, see theme.rcss); color is optional and tints the card's top line
--      and chosen border, the Slate accent otherwise.
--
--  Without a factions table the widget removes itself in Initialize; without
--  the gadget's "phase" param it waits only until the game starts, then goes.
--
--  While the chooser is on screen it sets WG.SlatePregame, which hides the
--  rest of the HUD (see hud.FollowGuiHidden in core.lua).
--------------------------------------------------------------------------------

local DOCUMENT_PATH = "factionchooser.rml"

-- the byte the spawn gadget's RecvLuaMsg listens for
local SPAWN_MSG_BYTE = "\138"

-- must match .card and .card.second in factionchooser.rml: cards of 420
-- with 40 between
local CARD_WIDTH   = 420
local CARD_GAP     = 40
local GROUP_HEIGHT = 500

local LAYOUT_NAME = "slate_factionchooser"

local DEADLINE_FRAME    = 900 -- fallback, matching CHOICE_TIMEOUT_FRAMES in game_spawn.lua
local COUNTDOWN_TOTAL   = 30  -- seconds the full bar stands for
local COUNTDOWN_BEEP_AT = 10  -- tick sound, and red, for the last seconds

local BORDER_IDLE = "rgba(255,255,255,60)"

local spSendLuaRulesMsg = Spring.SendLuaRulesMsg

local hud, S
local document
local view

local factions = {}         -- from slate_game.lua: id, name, blurb, picture, color
local groupWidth = 0        -- all the cards and the gaps between them

local chosen         = false -- true once the local player's choice has been sent
local chosenID       = nil
local hovered        = nil   -- index of the card under the mouse
local gameStarted    = false -- true once the game frame is past 0
local isSpectator    = false
local secondsLeft    = COUNTDOWN_TOTAL
local lastBeepSecond = nil

--------------------------------------------------------------------------------
-- showing
--------------------------------------------------------------------------------

local function Accent(faction)
	return faction.color or S.AccentColor()
end

local function CardsRML()
	local parts = {}
	for i, faction in ipairs(factions) do
		local picture = ""
		if faction.picture and faction.picture ~= "" then
			picture = string.format('<img class="hero" src="/%s"/>', faction.picture)
		else
			picture = '<div class="hero"/>'
		end
		parts[i] = string.format(
			'<div id="card%d" class="card panel%s" data-card="%d">'
			.. '<div class="topline" style="background-color: %s;"/>'
			.. '<div class="cname title">%s</div>'
			.. picture
			.. '<div class="cdesc">%s</div>'
			.. '<div id="card%d-state" class="cstate label">Choose</div>'
			.. '</div>',
			i, (i > 1) and " second" or "", i, Accent(faction), hud.Escape(faction.name or faction.id), hud.Escape(faction.blurb or ""), i)
	end
	return table.concat(parts)
end

local function Refresh()
	view.SetClass("root", "hidden", not gameStarted)
	if not gameStarted then
		return
	end
	view.SetClass("dim", "spectator", isSpectator)
	view.SetClass("cards", "hidden", isSpectator)
	view.SetText("title", isSpectator and "Players Are Choosing Their Factions" or "Choose Your Faction")

	local urgent = secondsLeft <= COUNTDOWN_BEEP_AT
	view.SetText("timer", secondsLeft .. "s")
	view.SetClass("timer", "urgent", urgent)
	view.SetClass("timer-fill", "urgent", urgent)
	local fraction = math.max(0, math.min(1, secondsLeft / COUNTDOWN_TOTAL))
	view.SetStyle("timer-fill", "width", string.format("%.1f%%", fraction * 100))

	if isSpectator then
		return
	end
	for i, faction in ipairs(factions) do
		local id = "card" .. i
		local isChosen = chosen and faction.id == chosenID
		-- once a faction is chosen the other cards no longer answer the mouse
		local lit = isChosen or (not chosen and hovered == i)
		view.SetStyle(id, "border-color", lit and Accent(faction) or BORDER_IDLE)
		view.SetClass(id, "chosen", isChosen)
		view.SetClass(id, "passed", chosen and not isChosen)
		view.SetText(id .. "-state", isChosen and "Chosen" or "Choose")
	end
end

--------------------------------------------------------------------------------
-- choosing
--------------------------------------------------------------------------------

-- Sends the choice. Returns true when it went out.
local function Choose(index)
	local faction = factions[index]
	local def = faction and UnitDefNames[faction.id]
	if not def or not def.id then
		return false
	end
	spSendLuaRulesMsg(SPAWN_MSG_BYTE .. def.id)
	chosen   = true
	chosenID = faction.id
	return true
end

local function AutoPickFaction()
	Choose(math.random(1, #factions))
end

--------------------------------------------------------------------------------
-- widget api
--------------------------------------------------------------------------------

local function DefaultOrigin(vsx, vsy, w, h, scale)
	return (vsx - w) * 0.5, (vsy - h) * 0.5
end

local function Place()
	local chooser = view.Element("chooser")
	chooser.style["width"] = groupWidth .. "dp"
	view.Element("heading").style["width"] = groupWidth .. "dp"
	view.ForgetStyles()
	hud.PlacePanel(chooser, LAYOUT_NAME, groupWidth, GROUP_HEIGHT, DefaultOrigin)
end

-- the job is done: Shutdown clears WG.SlatePregame so the HUD comes back
local function Leave()
	widgetHandler:RemoveWidget(widget)
end

function widget:Initialize()
	S = WG.Slate
	if not S then
		widgetHandler:RemoveWidget(widget)
		return
	end
	-- a game with no factions has no use for this widget
	factions = S.game.factions or {}
	if #factions == 0 then
		widgetHandler:RemoveWidget(widget)
		return
	end
	groupWidth = CARD_WIDTH * #factions + CARD_GAP * (#factions - 1)

	local helpers = include("slate/rml/core.lua")
	local result, reason = helpers.LoadDocument(DOCUMENT_PATH, widget)
	if not result then
		Spring.Echo("[Slate Faction Chooser] " .. tostring(reason))
		widgetHandler:RemoveWidget(widget)
		return
	end
	hud = helpers
	document = result
	isSpectator = Spring.GetSpectatingState()

	view = hud.NewView(document)
	view.Assume("root", "hidden", true) -- set in the markup
	view.Element("cards").inner_rml = CardsRML()

	local cards = view.Element("cards")
	cards:AddEventListener("mousedown", function(event)
		if chosen or isSpectator or not gameStarted then
			return
		end
		local index = hud.EventAttribute(event, "data-card")
		if index and event.parameters and event.parameters.button == 0 and Choose(index) then
			hud.Sound("click")
			Refresh()
		end
	end)
	cards:AddEventListener("mouseover", function(event)
		local index = hud.EventAttribute(event, "data-card")
		if index ~= hovered then
			hovered = index
			if index and not chosen then
				hud.Sound("hover")
			end
			Refresh()
		end
	end)
	cards:AddEventListener("mouseout", function()
		if hovered then
			hovered = nil
			Refresh()
		end
	end)

	hud.RegisterPanel(LAYOUT_NAME, "Faction Chooser", Place)
	hud.OnChange(LAYOUT_NAME, Place)
	Place()
	hud.ShowPassive(document)
end

function widget:Shutdown()
	WG.SlatePregame = nil
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

function widget:GameStart()
	isSpectator = Spring.GetSpectatingState()
end

function widget:Update()
	if not document then
		return
	end
	-- nothing ticks until the game has started
	if not gameStarted then
		if Spring.GetGameFrame() > 0 then
			gameStarted = true
		end
		return
	end

	-- Once the phase is no longer "faction" (placement has started, or the
	-- game is already under way), the job here is done. No phase at all means
	-- no gadget: the game has started without a faction choice, so go too.
	local currentPhase = Spring.GetGameRulesParam("phase")
	if currentPhase ~= "faction" then
		Leave()
		return
	end
	-- the rest of the HUD stays hidden for as long as the choice is open
	WG.SlatePregame = true

	-- The gadget's deadline is the one that counts; it is shortened when
	-- every player has chosen early.
	local frame = Spring.GetGameFrame()
	local deadline = Spring.GetGameRulesParam("factionDeadlineFrame") or DEADLINE_FRAME
	local framesLeft = math.max(0, deadline - frame)
	local gameSpeed = Spring.GetGameSpeed() or 1
	secondsLeft = math.ceil(framesLeft / (30 * gameSpeed))

	if secondsLeft <= COUNTDOWN_BEEP_AT and secondsLeft ~= lastBeepSecond and secondsLeft > 0 then
		hud.Sound("hover", 0.6)
		lastBeepSecond = secondsLeft
	end

	if framesLeft == 0 then
		-- out of time: a player who has not chosen gets a faction at random
		if not isSpectator and not chosen then
			AutoPickFaction()
		end
		-- (the phase change above is the usual way out; this is the fallback)
		Leave()
		return
	end

	Refresh()
end
