if addon.InGetInfo then
	return {
		name    = "Main",
		desc    = "The loading panel: a tip, quote or unit note (with a picture), the load message and a progress bar",
		author  = "jK; Splinter Faction; Scary le Poo",
		date    = "2012,2013; 2026",
		license = "GPL2",
		layer   = 0,
		depend  = {"LoadProgress"},
		enabled = true,
	}
end

--------------------------------------------------------------------------------
-- Splinter Faction's loading panel, drawn as a Slate window (see the look section below). The cards (tips, unit
-- notes, quotes) are data in LuaIntro/Configs/loadscreen.lua.
-- Engine settings that must be in place while loading are set by the Initial Settings addon (initial_settings.lua).
--------------------------------------------------------------------------------

local defaultFont = 'Saira_SemiCondensed-SemiBold.ttf'
local fontfile = 'luaui/fonts/' .. Spring.GetConfigString("ui_font", defaultFont)
if not VFS.FileExists(fontfile) then
	fontfile = 'luaui/fonts/' .. defaultFont
end
local boldfile = 'luaui/fonts/Saira_SemiCondensed-Bold.ttf'
if not VFS.FileExists(boldfile) then
	boldfile = fontfile
end

local showTips = true
local ok, cards = pcall(VFS.Include, "LuaIntro/Configs/loadscreen.lua")
if not ok or type(cards) ~= "table" then
	Spring.Echo("[LuaIntro] could not read LuaIntro/Configs/loadscreen.lua: " .. tostring(cards))
	cards = {}
end
local tips = cards.tips or {}
local unit_descs = cards.units or {}
local quotes = cards.quotes or {}
if #tips + #unit_descs + #quotes == 0 then
	showTips = false
end

-- math.random gives the same sequence every launch here, so a counter kept in
-- a file decides what is shown: it moves on by one each time the game loads.
local filename = "LuaUI/Config/randomseed.data"
local k = os.time() % 1500
if VFS.FileExists(filename) then
	k = tonumber(VFS.LoadFile(filename)) or k
end
k = k + 1
do
	local file = io.open(filename, 'w')
	if file then
		file:write(k)
		file:close()
	end
end

-- odd launches: a tip. Even launches: a quote on some, a unit note on the rest.
local card
local useTip = k % 2 == 1 or (#quotes == 0 and #unit_descs == 0)
local useQuote = not useTip and (#unit_descs == 0 or (k % 3 == 2 and #quotes > 0))
if not showTips then
	card = { kind = "", text = "" }
elseif useTip and #tips > 0 then
	local tip = tips[(math.ceil(k / 2) % #tips) + 1]
	card = { kind = "TIP", image = tip.image, title = tip.title, text = tip.text, link = tip.link }
elseif useQuote or #unit_descs == 0 then
	local quote = quotes[(math.ceil(k / 3) % #quotes) + 1]
	card = { kind = "QUOTE", text = quote[1], author = quote[2] }
else
	local desc = unit_descs[(math.floor(k / 2) % #unit_descs) + 1]
	card = { kind = "UNIT", image = desc.image, title = desc.title, text = desc.text }
end
card.text = card.text or ""
if card.image and not VFS.FileExists(card.image) then
	card.image = nil
end

--------------------------------------------------------------------------------
-- look: a Slate window (luaui/slate/rml/theme.rcss): dark glass with 8dp corners and a faint white border, a head
-- with the card kind as a .title (accent capitals) and the map as a .label, a rule under it, the picture in a
-- .raised tile, and below, a .label / .value pair over Slate's 6dp rounded progress bar. The player's Slate colour
-- tint and panel opacity (engine config slate_tint, slate_tintstrength, slate_opacity) are applied as Slate does
-- (slate_api_core.lua S.Colors); windows never go below 88% opacity.
--------------------------------------------------------------------------------

local theme = {}
do
	local okTheme, t = pcall(VFS.Include, "luaui/slate/configs/slate_theme.lua")
	if okTheme and type(t) == "table" then
		theme = t
	end
end
local basePanel  = theme.panel  or {0.050, 0.055, 0.063}
local baseBorder = theme.border or {1, 1, 1, 0.14}
local baseAccent = theme.accent or {0.663, 0.741, 0.816, 1}

local function Mix(a, b, t)
	return a * (1 - t) + b * t
end

local COLOR = {}
do
	local tintName = Spring.GetConfigString("slate_tint", theme.tint or "None")
	local tint
	for _, t in ipairs(theme.tints or {}) do
		if t.name == tintName then
			tint = t.color
		end
	end
	local strength = tint and math.max(0, math.min(1, Spring.GetConfigFloat("slate_tintstrength", theme.tintStrength or 0.5) or 0.5)) or 0
	tint = tint or {0, 0, 0}
	local panel, border, accent = {}, {}, {}
	for i = 1, 3 do
		local light = tint[i] * 0.55 + 0.45
		panel[i]  = Mix(basePanel[i], tint[i] * 0.38, strength)
		border[i] = Mix(baseBorder[i], light, strength)
		accent[i] = Mix(baseAccent[i], light, strength)
	end
	local opacity = Spring.GetConfigFloat("slate_opacity", theme.opacity or 0.6) or 0.6
	COLOR.panel  = {panel[1], panel[2], panel[3], math.max(opacity, 0.88)}   -- .panel.window
	COLOR.border = {border[1], border[2], border[3], baseBorder[4] or 0.14}  -- rgba(255,255,255,36)
	COLOR.raised = {1, 1, 1, 18 / 255}                                       -- .raised / .tile
	COLOR.raisedBorder = {1, 1, 1, 33 / 255}
	COLOR.track  = {1, 1, 1, 26 / 255}                                       -- .bar
	COLOR.accent = {accent[1], accent[2], accent[3], 1}                      -- .bar-fill, .title
	COLOR.rule   = {1, 1, 1, 36 / 255}                                       -- .window-head border
end

-- inline text colours
local function TextColor(r, g, b)
	return "\255" .. string.char(math.max(1, math.floor(r)), math.max(1, math.floor(g)), math.max(1, math.floor(b)))
end
local TEXT = {
	text    = TextColor(0xec, 0xee, 0xf0),
	heading = TextColor(0xf4, 0xf5, 0xf7),
	muted   = TextColor(0xb5, 0xba, 0xc1),
	dimmer  = TextColor(0x8a, 0x90, 0x99),
	accent  = TextColor(COLOR.accent[1] * 255, COLOR.accent[2] * 255, COLOR.accent[3] * 255),
}

-- Sizes are in dp: pixels of a 1080-pixel-high screen, scaled from there.
local PANEL_WIDTH_FRAC = 0.60  -- share of the screen's width...
local PANEL_MIN_WIDTH  = 760   -- ...but not narrower than this
local PANEL_BOTTOM_FRAC = 0.075 -- gap under the panel, as a share of the screen's height
local PAD         = 16         -- inside the panel (Slate windows: 14-16dp)
local RADIUS      = 8          -- panel corners
local TILE_RADIUS = 5          -- tile corners
local HEAD_HEIGHT = 30         -- the window head, down to its rule
local CARD_GAP    = 12         -- above and below the card's content (it is as tall as its text or picture)
local BAR_HEIGHT  = 72         -- the load message, percentage and bar
local IMAGE_SIZE  = 96
local MAX_TEXT_LINES = 4

--------------------------------------------------------------------------------
-- progress
--------------------------------------------------------------------------------

local lastLoadMessage = ""
local lastProgress = {0, 0}

-- The engine reports stages, not a percentage. Each stage is given a range,
-- and the time the last load of this map took (LoadProgress) moves the bar
-- inside it.
local progressByLastLine = {
	["Parsing Map Information"] = {0, 20},
	["Loading Weapon Definitions"] = {10, 50},
	["Loading LuaRules"] = {40, 80},
	["Loading LuaUI"] = {70, 95},
	["Finalizing"] = {100, 100}
}
for name,val in pairs(progressByLastLine) do
	progressByLastLine[name] = {val[1]*0.01, val[2]*0.01}
end

function addon.LoadProgress(message, replaceLastLine)
	lastLoadMessage = message
	if message:find("Path") then -- pathing has no rigid messages so cant use the table
		lastProgress = {0.8, 1.0}
	end
	lastProgress = progressByLastLine[message] or lastProgress
end

--------------------------------------------------------------------------------
-- drawing, in screen pixels (y up)
--------------------------------------------------------------------------------

local LOADED_FONT_SIZE = 48
local font     = gl.LoadFont(fontfile, LOADED_FONT_SIZE, 2, 1)
local boldFont = gl.LoadFont(boldfile, LOADED_FONT_SIZE, 2, 1)
if not boldFont then
	boldFont = font
end

local floor = math.floor
local canRound = gl.BeginEnd and GL and GL.TRIANGLE_FAN and GL.TRIANGLE_STRIP

local function SetColor(color, alpha)
	gl.Color(color[1], color[2], color[3], alpha or color[4] or 1)
end

-- the outline of a rounded rectangle, counter-clockwise from the bottom-left corner's start
local CORNER_STEPS = 8
local function Contour(x1, y1, x2, y2, r)
	local pts = {}
	local corners = {
		{x1 + r, y1 + r, math.pi, 1.5 * math.pi},        -- bottom left
		{x2 - r, y1 + r, 1.5 * math.pi, 2 * math.pi},    -- bottom right
		{x2 - r, y2 - r, 0, 0.5 * math.pi},              -- top right
		{x1 + r, y2 - r, 0.5 * math.pi, math.pi},        -- top left
	}
	for _, c in ipairs(corners) do
		for i = 0, CORNER_STEPS do
			local a = c[3] + (c[4] - c[3]) * i / CORNER_STEPS
			pts[#pts + 1] = {c[1] + math.cos(a) * r, c[2] + math.sin(a) * r}
		end
	end
	return pts
end

-- a filled rounded rectangle
local function RoundRect(x1, y1, x2, y2, r, color)
	SetColor(color)
	r = math.min(r, (x2 - x1) * 0.5, (y2 - y1) * 0.5)
	if not canRound or r < 1 then
		gl.Rect(x1, y1, x2, y2)
		return
	end
	local pts = Contour(x1, y1, x2, y2, r)
	gl.BeginEnd(GL.TRIANGLE_FAN, function()
		gl.Vertex((x1 + x2) * 0.5, (y1 + y2) * 0.5)
		for i = 1, #pts do
			gl.Vertex(pts[i][1], pts[i][2])
		end
		gl.Vertex(pts[1][1], pts[1][2])
	end)
end

-- a rounded border of width w, inside the rectangle (an RmlUi border)
local function RoundBorder(x1, y1, x2, y2, r, w, color)
	SetColor(color)
	if not canRound or r < 1 then
		gl.Rect(x1, y1, x2, y1 + w)
		gl.Rect(x1, y2 - w, x2, y2)
		gl.Rect(x1, y1 + w, x1 + w, y2 - w)
		gl.Rect(x2 - w, y1 + w, x2, y2 - w)
		return
	end
	local outer = Contour(x1, y1, x2, y2, r)
	local inner = Contour(x1 + w, y1 + w, x2 - w, y2 - w, math.max(0, r - w))
	gl.BeginEnd(GL.TRIANGLE_STRIP, function()
		for i = 1, #outer do
			gl.Vertex(outer[i][1], outer[i][2])
			gl.Vertex(inner[i][1], inner[i][2])
		end
		gl.Vertex(outer[1][1], outer[1][2])
		gl.Vertex(inner[1][1], inner[1][2])
	end)
end

-- Slate's small capitals: upper case, spaced out (RmlUi letter-spacing). align "l" or "r"
local function SpacedWidth(useFont, text, size, spacing)
	local w = 0
	for i = 1, #text do
		w = w + useFont:GetTextWidth(text:sub(i, i)) * size
	end
	return w + spacing * math.max(0, #text - 1)
end

local function PrintSpaced(useFont, color, text, x, y, size, spacing, align)
	text = string.upper(text)
	if align == "r" then
		x = x - SpacedWidth(useFont, text, size, spacing)
	end
	for i = 1, #text do
		local ch = text:sub(i, i)
		useFont:Print(color .. ch, x, y, size, "a")
		x = x + useFont:GetTextWidth(ch) * size + spacing
	end
end

-- Wraps text to a width in pixels at a font size; keeps at most maxLines lines.
local function Wrap(useFont, text, width, size, maxLines)
	local wrapped = useFont:WrapText(text, width * (LOADED_FONT_SIZE / size))
	local lines = {}
	for line in (wrapped .. "\n"):gmatch("(.-)\r?\n") do
		lines[#lines + 1] = line
		if #lines == maxLines then
			break
		end
	end
	return lines
end

local cardHeight

local KIND_NAME = { TIP = "Tip", UNIT = "Unit", QUOTE = "Quote" }

-- the window head: the card kind (.title) and the map (.label), then the rule
local function DrawHead(x1, y2, x2, s, line)
	local pad = PAD * s
	-- (text is placed by its top: font option "a")
	local top = y2 - pad - 3 * s
	PrintSpaced(boldFont, TEXT.accent, KIND_NAME[card.kind] or card.kind, x1 + pad, top, 14 * s, 2 * s, "l")
	if Game and Game.mapName then
		PrintSpaced(font, TEXT.muted, Game.mapName, x2 - pad, top - 3 * s, 11 * s, 1.5 * s, "r")
	end
	local ruleY = floor(y2 - pad - HEAD_HEIGHT * s)
	SetColor(COLOR.rule)
	gl.Rect(x1 + pad, ruleY, x2 - pad, ruleY + line)
	return ruleY
end

-- the card's text, wrapped to the space beside the picture
local function CardText(x1, x2, s)
	local pad = PAD * s
	local left = x1 + pad + (card.image and (floor(IMAGE_SIZE * s) + pad) or 0)
	local quote = card.kind == "QUOTE"
	local size = quote and 18 * s or 15 * s
	local lines = Wrap(font, card.text, (x2 - pad) - left, size, card.title and (MAX_TEXT_LINES - 1) or MAX_TEXT_LINES)
	return lines, size, size * 1.38
end

-- height of the card under the head's rule: its content and a gap either side
local function CardHeight(x1, x2, s)
	local lines, _, lineHeight = CardText(x1, x2, s)
	local text = (card.title and 27 * s or 0) + #lines * lineHeight + (card.link and 18 * s or 0) + (card.author and 20 * s or 0)
	local image = card.image and floor(IMAGE_SIZE * s) or 0
	return floor(2 * CARD_GAP * s + math.max(text, image))
end

local function DrawCard(x1, y1, x2, top, s, line)
	local pad = PAD * s
	local left = x1 + pad
	top = top - CARD_GAP * s

	if card.image then
		local size = floor(IMAGE_SIZE * s)
		local t = floor(top)
		RoundRect(left, t - size, left + size, t, TILE_RADIUS * s, COLOR.raised)
		gl.Color(1, 1, 1, 1)
		gl.Texture(":n:" .. card.image)
		gl.TexRect(left + 3 * s, t - size + 3 * s, left + size - 3 * s, t - 3 * s, false, false)
		gl.Texture(false)
		RoundBorder(left, t - size, left + size, t, TILE_RADIUS * s, line, COLOR.raisedBorder)
		left = left + size + pad
	end

	if card.title then
		boldFont:Print(TEXT.heading .. card.title, left, top, 19 * s, "a")
		top = top - 27 * s
	end
	local quote = card.kind == "QUOTE"
	local lines, size, lineHeight = CardText(x1, x2, s)
	for i, l in ipairs(lines) do
		font:Print((quote and TEXT.heading or TEXT.text) .. l, left, top - (i - 1) * lineHeight, size, "a")
	end
	top = top - #lines * lineHeight
	if card.link then
		font:Print(TEXT.accent .. card.link, left, top - 2 * s, 13 * s, "a")
	end
	if card.author then
		font:Print(TEXT.muted .. "- " .. card.author, x2 - pad, top - 6 * s, 13 * s, "ar")
	end
end

-- a .label over the load message (.sub), the percentage as a .value, then the bar
local function DrawBar(x1, y1, x2, y2, s, loadProgress, line)
	local pad = PAD * s
	local top = y2 - 14 * s

	PrintSpaced(font, TEXT.muted, "Loading", x1 + pad, top, 11 * s, 1.5 * s, "l")
	local message = lastLoadMessage
	if message ~= "" then
		font:Print(TEXT.dimmer .. message, x1 + pad, top - 17 * s, 12 * s, "a")
	end
	boldFont:Print(TEXT.heading .. ("%.0f%%"):format(math.max(0, loadProgress) * 100), x2 - pad, top + 2 * s, 21 * s, "ar")

	local barH = math.max(4, floor(6 * s))
	local barY1 = floor(y1 + pad)
	local barX1, barX2 = floor(x1 + pad), floor(x2 - pad)
	RoundRect(barX1, barY1, barX2, barY1 + barH, barH * 0.5, COLOR.track)
	local fill = math.max(0, math.min(1, loadProgress))
	if fill > 0 then
		RoundRect(barX1, barY1, math.max(barX1 + barH, barX1 + (barX2 - barX1) * fill), barY1 + barH, barH * 0.5, COLOR.accent)
	end
end

function addon.DrawLoadScreen()
	local loadProgress = SG.GetLoadProgress()
	if loadProgress == 0 then
		loadProgress = lastProgress[1]
	else
		loadProgress = math.min(math.max(loadProgress, lastProgress[1]), lastProgress[2])
	end

	local vsx, vsy = gl.GetViewSizes()
	local s = vsy / 1080

	local width = floor(math.min(vsx - 2 * PAD * s, math.max(vsx * PANEL_WIDTH_FRAC, PANEL_MIN_WIDTH * s)))
	local barH = floor(BAR_HEIGHT * s)
	local x1 = floor((vsx - width) * 0.5)
	local x2 = x1 + width
	cardHeight = cardHeight or (showTips and CardHeight(x1, x2, s))   -- the text does not change while loading
	local cardH = showTips and (floor((PAD + HEAD_HEIGHT) * s) + cardHeight) or 0
	local y1 = floor(vsy * PANEL_BOTTOM_FRAC)
	local y2 = y1 + barH + cardH
	local line = math.max(1, floor(s + 0.5))

	-- the load screen is drawn in 0..1 coordinates; work in pixels instead
	gl.PushMatrix()
	gl.Scale(1 / vsx, 1 / vsy, 1)
	gl.Texture(false)

	RoundRect(x1, y1, x2, y2, RADIUS * s, COLOR.panel)
	RoundBorder(x1, y1, x2, y2, RADIUS * s, line, COLOR.border)

	if showTips then
		local ruleY = DrawHead(x1, y2, x2, s, line)
		DrawCard(x1, y1 + barH, x2, ruleY, s, line)
		-- between the card and the bar
		SetColor(COLOR.rule)
		gl.Rect(x1 + PAD * s, y1 + barH, x2 - PAD * s, y1 + barH + line)
	end
	DrawBar(x1, y1, x2, y1 + barH, s, loadProgress, line)

	gl.Color(1, 1, 1, 1)
	gl.PopMatrix()
end


function addon.MousePress(...)
	--Spring.Echo(...)
end


function addon.Shutdown()
	gl.DeleteFont(font)
	if boldFont ~= font then
		gl.DeleteFont(boldFont)
	end
end
