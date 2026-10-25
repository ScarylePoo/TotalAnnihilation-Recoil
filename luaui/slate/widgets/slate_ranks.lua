-- Part of Slate, a game-neutral RmlUi interface for Total Annihilation style
-- games on the Recoil engine. Derived from the Bastion HUD in Splinter
-- Faction (same author, GPL v2+).

function widget:GetInfo()
	return {
		name    = "Slate Ranks",
		desc    = "Per-match rank tracks: the strip and the rank-up card",
		author  = "Scary le Poo; SplinterFaction Team",
		date    = "2026-10-24",
		license = "GNU GPL, v2 or later",
		layer   = -1990,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
--  Rank tracks. A gadget counts a few things per team (metal destroyed,
--  sustained income, metal built, extractors held) and hands out cosmetic
--  ranks. This widget shows them:
--
--    the strip, top right: the viewed team's rank on each track with a bar
--    to the next one, read from the team rules params the gadget publishes;
--
--    the card, under the resource bar: a badge that slams in when a rank is
--    reached, holds a moment, and fades. Rank-ups arrive from the gadget as
--    RankUpEvent and are queued, so two reached in the same fight play one
--    after the other instead of on top of each other.
--
--  Players only: a spectator sees nothing of it, and neither does a replay.
--  Nothing here affects play. The widget can be switched off in Options.
--
--  WHAT A GAME MUST PROVIDE
--
--  A game without a rank gadget need do nothing: the widget sees no rank
--  params and removes itself quietly. A game that wants ranks provides:
--
--    the track config, luaui/slate/configs/slate_ranks.lua (a game's own
--    copy in luaui/configs/ wins): tracks = { {id=, name=, unit=, thresholds=,
--    titles=}, ... } and optionally upgrades = { {id=, name=, param=, effect=,
--    mults=, titles=}, ... }. The gadget should read the same file;
--
--    a gadget (game_rank_tracks.lua in the game it came from) that, for every
--    player team, sets the team rules params rank_<track id>_level and
--    rank_<track id>_value (from its Initialize on, so a reload finds them);
--    scales the "territory" track to the map and publishes the result as the
--    game rules params rank_territory_t<rank>; and on each rank reached
--    calls the unsynced global RankUpEvent(teamID, trackIndex, level, value)
--    in LuaUI (Script.LuaUI.RankUpEvent);
--
--    an emblem per track and upgrade, luaui/slate/images/rank_<id>.png,
--    and rank_chevron.png / rank_chevron_ember.png for the tally
--    (premultiplied alpha, see theme.rcss);
--
--    optionally a sound: "rankup" in the sounds table of slate_game.lua, or
--    "rankup1".."rankup5" for one per rank. No entry means silence.
--
--  An upgrade (from an upgrades gadget mirroring upgrade_<id>_level team
--  rules params) gets a card too, though no place in the strip.
--------------------------------------------------------------------------------

local DOCUMENT_PATH = "ranks.rml"
local CONFIG_FILE   = "slate_ranks.lua"
-- a game's own copy in luaui/configs/ wins, as with the other Slate configs
local CONFIG_DIRS   = { LUAUI_DIRNAME .. "configs/", LUAUI_DIRNAME .. "slate/configs/" }

-- must match #ranks and #rankup in ranks.rml
local STRIP_WIDTH  = 250
local STRIP_HEIGHT = 160
-- the menu button's height, so the strip sits under it, right-aligned with
-- it: must match BUTTON_HEIGHT in slate_menu.lua
local MENU_BUTTON_HEIGHT = 30
local CARD_WIDTH   = 320
local CARD_HEIGHT  = 252
-- the card goes below the resource bar: must match BAR_HEIGHT in slate_resourcebar.lua
local RESBAR_HEIGHT = 64

local LAYOUT_STRIP = "slate_ranks"
local LAYOUT_CARD  = "slate_rankup"

-- the card's timing, in seconds
local SLAM_TIME   = 0.22  -- coming in: from oversized and clear to in place
local HOLD_TIME   = 2.2   -- fully shown
local FADE_TIME   = 0.45  -- going away
local GAP_TIME    = 0.5   -- between two cards
local FADE_STEPS  = 20    -- opacity moves in this many steps (as the pause banner does)

local STRIP_PERIOD = 15   -- frames between strip refreshes; matches the gadget

local SOUND_VOLUME = 0.8

local ROMAN = {"I", "II", "III", "IV", "V"}

--------------------------------------------------------------------------------
-- state
--------------------------------------------------------------------------------

local hud, S
local document
local view

local tracks = {}    -- from the config: id, name, unit, thresholds, titles
local upgrades = {}  -- from the config: id, name, param, effect, mults, titles
local upgradeLevels  -- last seen level per upgrade, nil until the first poll

local queue = {}   -- rank-ups waiting to be shown: {track, level, value} or {upgrade, level}
local card  = nil  -- the one being shown: {track, level, value, t0}
local cardShownAt = -1 -- when the last card ended, for the gap

local fresh = nil  -- track index with the latest rank-up, highlighted in the strip
local freshUntil = 0

local viewedTeam = Spring.GetMyTeamID()
local isSpec = Spring.GetSpectatingState()
local lastStripFrame = -1

--------------------------------------------------------------------------------
-- helpers
--------------------------------------------------------------------------------

local startTimer = Spring.GetTimer()

-- seconds since the widget started
local function Now()
	return Spring.DiffTimers(Spring.GetTimer(), startTimer)
end

-- 6300 -> "6.3k", 420 -> "420", 12.5 -> "12.5"
local function Short(n)
	if n >= 10000 then
		return string.format("%dk", math.floor(n / 1000 + 0.5))
	elseif n >= 1000 then
		return string.format("%.1fk", n / 1000)
	elseif n >= 100 or n == math.floor(n) then
		return tostring(math.floor(n + 0.5))
	end
	return string.format("%.1f", n)
end

-- what the card says under the title, in the track's own units
local function Achievement(track, value)
	if track.unit == "metal" then
		if track.id == "combat" then
			return hud.Number(value) .. " metal of enemy units destroyed"
		end
		return hud.Number(value) .. " metal of units built"
	elseif track.unit == "income" then
		return "+" .. Short(value) .. " sustained income"
	elseif track.unit == "extractors" then
		return value .. " extractors held"
	end
	return tostring(value)
end

-- what the strip says under the bar: how far to the next rank
local function ToNext(track, level, value)
	local thresholds = track.thresholds
	if level >= #thresholds then
		return "max"
	end
	local gap = math.max(0, thresholds[level + 1] - value)
	local target = ROMAN[level + 1] or tostring(level + 1)
	if track.unit == "income" then
		return "+" .. Short(gap) .. " to " .. target
	end
	return Short(gap) .. " to " .. target
end

local function Progress(track, level, value)
	local thresholds = track.thresholds
	if level >= #thresholds then
		return 1
	end
	local from = level > 0 and thresholds[level] or 0
	local to = thresholds[level + 1]
	if to <= from then
		return 1
	end
	return math.max(0, math.min(1, (value - from) / (to - from)))
end

-- Spring.GetTeamRulesParam returns no values for an unset param, so the
-- double parentheses turn that into nil
local function TeamParam(teamID, name)
	return (Spring.GetTeamRulesParam(teamID, name))
end

-- true when some team carries the gadget's rank params: the gadget is there
local function GadgetPresent()
	local first = tracks[1]
	if not first then
		return false
	end
	for _, teamID in ipairs(Spring.GetTeamList()) do
		if TeamParam(teamID, "rank_" .. first.id .. "_level") ~= nil then
			return true
		end
	end
	return false
end

local function LoadConfig()
	for _, dir in ipairs(CONFIG_DIRS) do
		local path = dir .. CONFIG_FILE
		if VFS.FileExists(path) then
			local ok, config = pcall(VFS.Include, path)
			if ok and type(config) == "table" and type(config.tracks) == "table" then
				return config
			end
			Spring.Echo("[Slate Ranks] could not read " .. path)
			return nil
		end
	end
	return nil
end

-- a file in luaui/slate/images/; the leading slash makes the path absolute
-- instead of relative to the document
local function ImagePath(file)
	return "/" .. hud.IMAGE_DIR .. file
end

-- one sound per rank when the game names them, else the one "rankup"
local function RankSound(level)
	local sounds = S.game.sounds or {}
	local perRank = "rankup" .. level
	hud.Sound(sounds[perRank] and perRank or "rankup", SOUND_VOLUME)
end

--------------------------------------------------------------------------------
-- the strip
--------------------------------------------------------------------------------

-- the gadget scales the territory thresholds to the map; read them once
local territoryRead = false
local function ReadTerritoryThresholds()
	if territoryRead then
		return
	end
	for _, track in ipairs(tracks) do
		if track.id == "territory" then
			local thresholds = {}
			for rank = 1, #track.thresholds do
				local t = (Spring.GetGameRulesParam("rank_territory_t" .. rank))
				if not t then
					return
				end
				thresholds[rank] = tonumber(t)
			end
			track.thresholds = thresholds
		end
	end
	territoryRead = true
end

-- A bought upgrade shows up as a higher level param. The first reading sets
-- the baseline, so a reload mid-game does not replay every level bought so far.
local function PollUpgrades()
	if isSpec or #upgrades == 0 then
		return
	end
	local first = upgradeLevels == nil
	if first then
		upgradeLevels = {}
	end
	for i, upgrade in ipairs(upgrades) do
		local level = tonumber(TeamParam(viewedTeam, upgrade.param)) or 0
		local known = upgradeLevels[i]
		if first or known == nil then
			upgradeLevels[i] = level
		elseif level > known then
			for l = known + 1, level do
				queue[#queue + 1] = {upgrade = i, level = l}
			end
			upgradeLevels[i] = level
		elseif level < known then
			upgradeLevels[i] = level
		end
	end
end

local function RefreshStrip()
	ReadTerritoryThresholds()
	if isSpec then
		view.SetClass("ranks", "hidden", true)
		return
	end
	local teamID = viewedTeam
	local any = false
	for i, track in ipairs(tracks) do
		local level = TeamParam(teamID, "rank_" .. track.id .. "_level")
		local value = TeamParam(teamID, "rank_" .. track.id .. "_value")
		if level then
			any = true
			level = tonumber(level) or 0
			value = tonumber(value) or 0
			local max = level >= #track.thresholds
			view.SetText("lvl-" .. i, level > 0 and (ROMAN[level] or tostring(level)) or "-")
			view.SetClass("lvl-" .. i, "max", max)
			view.SetClass("lvl-" .. i, "none", level == 0)
			view.SetText("ttl-" .. i, hud.Escape(level > 0 and (track.titles and track.titles[level]) or "Unranked"))
			view.SetClass("ttl-" .. i, "max", max)
			view.SetClass("ttl-" .. i, "none", level == 0)
			view.SetStyle("fill-" .. i, "width", string.format("%d%%", math.floor(Progress(track, level, value) * 100 + 0.5)))
			view.SetText("next-" .. i, ToNext(track, level, value))
		end
		view.SetClass("cell-" .. i, "fresh", fresh == i)
	end
	view.SetClass("ranks", "hidden", not any)
end

--------------------------------------------------------------------------------
-- the card
--------------------------------------------------------------------------------

local function FillCard(entry)
	local level = entry.level
	local id, label, title, sub
	if entry.upgrade then
		local upgrade = upgrades[entry.upgrade]
		id = upgrade.id
		label = upgrade.name .. " · Level " .. (ROMAN[level] or tostring(level))
		title = upgrade.titles[level] or ("Level " .. level)
		local mult = upgrade.mults and upgrade.mults[level]
		sub = mult and string.format("+%d%% %s", math.floor((mult - 1) * 100 + 0.5), upgrade.effect)
			or (upgrade.effect .. " upgraded")
	else
		local track = tracks[entry.track]
		id = track.id
		label = track.name .. " · Rank " .. (ROMAN[level] or tostring(level))
		title = track.titles[level] or ("Rank " .. level)
		sub = Achievement(track, entry.value)
	end
	view.SetText("rankup-track-text", hud.Escape(label))
	view.SetText("rankup-title", hud.Escape(title))
	view.SetText("rankup-sub", hud.Escape(sub))
	local emblem = view.Element("rankup-emblem")
	if emblem then
		emblem:SetAttribute("src", ImagePath("rank_" .. id .. ".png"))
	end
	local tier = math.min(level, 5) -- the frame has five looks; upgrades go to six
	for t = 1, 5 do
		view.SetClass("rankup-frame", "t" .. t, t == tier)
	end
	local chevron = ImagePath(level >= 5 and "rank_chevron_ember.png" or "rank_chevron.png")
	local rml = {}
	for _ = 1, level do
		rml[#rml + 1] = '<img src="' .. chevron .. '"/>'
	end
	local tally = view.Element("rankup-chevrons")
	if tally then
		tally.inner_rml = table.concat(rml)
	end
end

local function StartCard(entry)
	card = entry
	card.t0 = Now()
	FillCard(entry)
	if entry.track then
		fresh = entry.track
		freshUntil = card.t0 + HOLD_TIME + FADE_TIME + 6
	end
	RankSound(entry.level)
	pcall(function() document:PullToFront() end)
	view.SetClass("rankup", "hidden", false)
	lastStripFrame = -1 -- so the strip shows the new rank at once
end

local function EndCard()
	card = nil
	cardShownAt = Now()
	view.SetClass("rankup", "hidden", true)
end

-- opacity and position over the card's life. Stepped like the pause banner,
-- so the document is not restyled every frame for a change nobody can see.
local function AnimateCard()
	local t = Now() - card.t0
	local opacity, lift
	if t < SLAM_TIME then
		local p = t / SLAM_TIME
		p = 1 - (1 - p) * (1 - p) -- ease out
		opacity = p
		lift = (1 - p) * 20 -- starts a little high and settles
	elseif t < SLAM_TIME + HOLD_TIME then
		opacity, lift = 1, 0
	elseif t < SLAM_TIME + HOLD_TIME + FADE_TIME then
		opacity = 1 - (t - SLAM_TIME - HOLD_TIME) / FADE_TIME
		lift = 0
	else
		EndCard()
		return
	end
	view.SetStyle("rankup", "opacity", string.format("%.2f", math.ceil(opacity * FADE_STEPS) / FADE_STEPS))
	view.SetStyle("rankup", "margin-top", string.format("%ddp", -math.floor(lift + 0.5)))
end

--------------------------------------------------------------------------------
-- events from the gadget
--------------------------------------------------------------------------------

local function RankUpEvent(teamID, trackIndex, level, value)
	if isSpec or teamID ~= viewedTeam or not tracks[trackIndex] then
		return
	end
	queue[#queue + 1] = {track = trackIndex, level = level, value = value}
end

--------------------------------------------------------------------------------
-- widget api
--------------------------------------------------------------------------------

local function StripOrigin(vsx, vsy, w, h, scale)
	local margin = hud.Margin() * scale
	return vsx - margin - w, vsy - margin - (MENU_BUTTON_HEIGHT + hud.Gap()) * scale - h
end

local function CardOrigin(vsx, vsy, w, h, scale)
	return (vsx - w) * 0.5, vsy - (hud.Margin() + RESBAR_HEIGHT + hud.Gap()) * scale - h
end

local function Place()
	hud.PlacePanel(view.Element("ranks"), LAYOUT_STRIP, STRIP_WIDTH, STRIP_HEIGHT, StripOrigin)
	hud.PlacePanel(view.Element("rankup"), LAYOUT_CARD, CARD_WIDTH, CARD_HEIGHT, CardOrigin)
	view.ForgetStyles()
	-- the card's border follows the accent, tint included
	view.SetStyle("rankup", "border-color", S.AccentColor())
end

function widget:Initialize()
	S = WG.Slate
	if not S or Spring.IsReplay() then
		widgetHandler:RemoveWidget(self)
		return
	end
	local config = LoadConfig()
	if not config then
		widgetHandler:RemoveWidget(self)
		return
	end
	tracks = config.tracks
	upgrades = config.upgrades or {}

	-- no rank params on any team: the game has no rank gadget
	if not GadgetPresent() then
		widgetHandler:RemoveWidget(self)
		return
	end

	local helpers = include("slate/rml/core.lua")
	local result, reason = helpers.LoadDocument(DOCUMENT_PATH, widget)
	if not result then
		Spring.Echo("[Slate Ranks] " .. tostring(reason))
		widgetHandler:RemoveWidget(self)
		return
	end
	hud = helpers
	document = result
	view = hud.NewView(document)
	view.Assume("ranks", "hidden", true)
	view.Assume("rankup", "hidden", true)
	for i = 1, 4 do
		view.Assume("lvl-" .. i, "none", true)
		view.Assume("ttl-" .. i, "none", true)
	end
	view.Assume("rankup-frame", "t1", true)

	widgetHandler:RegisterGlobal("RankUpEvent", RankUpEvent)

	hud.RegisterPanel(LAYOUT_STRIP, "Ranks", Place)
	hud.RegisterPanel(LAYOUT_CARD, "Rank-up", Place, function() return card ~= nil end)
	hud.OnChange(LAYOUT_STRIP, Place)
	Place()
	hud.ShowPassive(document)
	viewedTeam = Spring.GetMyTeamID()
	isSpec = Spring.GetSpectatingState()
	RefreshStrip()
end

function widget:Shutdown()
	widgetHandler:DeregisterGlobal("RankUpEvent")
	if hud then
		hud.UnregisterPanel(LAYOUT_STRIP)
		hud.UnregisterPanel(LAYOUT_CARD)
		hud.OffChange(LAYOUT_STRIP)
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

-- a player who resigns or dies becomes a spectator: the strip goes away and
-- pending cards are dropped
function widget:PlayerChanged(playerID)
	local teamID = Spring.GetMyTeamID()
	local spec = Spring.GetSpectatingState()
	if teamID ~= viewedTeam or spec ~= isSpec then
		viewedTeam = teamID
		isSpec = spec
		upgradeLevels = nil
		queue = {}
		if card then
			EndCard()
		end
		fresh = nil
		lastStripFrame = -1
	end
end

function widget:GameFrame(n)
	if n - lastStripFrame >= STRIP_PERIOD or lastStripFrame < 0 then
		lastStripFrame = n
		if document and not Spring.IsGUIHidden() then
			if fresh and Now() > freshUntil then
				fresh = nil
			end
			RefreshStrip()
			PollUpgrades()
		end
	end
end

function widget:Update()
	if not document then
		return
	end
	if hud.FollowGuiHidden(document) then
		return
	end
	if card then
		AnimateCard()
	elseif #queue > 0 and Now() - cardShownAt >= GAP_TIME then
		StartCard(table.remove(queue, 1))
	end
end
