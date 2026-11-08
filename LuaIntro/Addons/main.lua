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
-- Splinter Faction's loading panel in Slate's look (luaui/slate/configs/slate_theme.lua: dark glass, a faint white
-- border, the pale steel accent). The cards (tips, unit notes, quotes) are data in LuaIntro/Configs/loadscreen.lua.
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
-- look: Slate's palette (slate_theme.lua / theme.rcss). Square panels with two accent corner brackets.
--------------------------------------------------------------------------------

local COLOR = {
	panel   = {0.050, 0.055, 0.063, 0.90}, -- Slate panel glass
	raised  = {0.115, 0.125, 0.140, 1},
	border  = {0.200, 0.210, 0.225, 1},    -- white at 14% over the glass
	firm    = {0.300, 0.320, 0.345, 1},
	ember   = {0.663, 0.741, 0.816, 1},    -- Slate's accent (pale steel)
}
-- inline text colors
local function TextColor(r, g, b)
	return "\255" .. string.char(math.max(1, r), math.max(1, g), math.max(1, b))
end
local TEXT = {
	body    = TextColor(200, 206, 214),
	heading = TextColor(240, 244, 248),
	muted   = TextColor(133, 142, 154),
	ember   = TextColor(169, 189, 208),   -- accent
	dimEmber = TextColor(135, 152, 170),
	signal  = TextColor(95, 208, 232),
}

-- Sizes are in pixels of a 1080-pixel-high screen and scale from there.
local PANEL_WIDTH_FRAC = 0.60  -- share of the screen's width...
local PANEL_MIN_WIDTH  = 760   -- ...but not narrower than this
local PANEL_BOTTOM_FRAC = 0.075 -- gap under the panel, as a share of the screen's height
local CARD_HEIGHT = 152  -- the tip, quote or unit note
local BAR_HEIGHT  = 66   -- the load message, percentage and bar
local PAD         = 18
local IMAGE_SIZE  = 96
local MAX_TEXT_LINES = 4

local LOADED_FONT_SIZE = 48
local font     = gl.LoadFont(fontfile, LOADED_FONT_SIZE, 2, 1)
local boldFont = gl.LoadFont(boldfile, LOADED_FONT_SIZE, 2, 1)
if not boldFont then
	boldFont = font
end

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

local function Rect(x1, y1, x2, y2, color, alpha)
	gl.Color(color[1], color[2], color[3], alpha or color[4] or 1)
	gl.Rect(x1, y1, x2, y2)
end

-- a one-pixel-wide outline, drawn inside the rectangle
local function Outline(x1, y1, x2, y2, color, width)
	Rect(x1, y1, x2, y1 + width, color)
	Rect(x1, y2 - width, x2, y2, color)
	Rect(x1, y1, x1 + width, y2, color)
	Rect(x2 - width, y1, x2, y2, color)
end

-- the two ember corner brackets: top left and bottom right
local function Brackets(x1, y1, x2, y2, length, width)
	Rect(x1, y2 - width, x1 + length, y2, COLOR.ember)
	Rect(x1, y2 - length, x1 + width, y2, COLOR.ember)
	Rect(x2 - length, y1, x2, y1 + width, COLOR.ember)
	Rect(x2 - width, y1, x2, y1 + length, COLOR.ember)
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

local function DrawCard(x1, y1, x2, y2, s)
	local pad = PAD * s
	local left = x1 + pad
	local top = y2 - pad

	-- what kind of card this is, and the map being loaded
	font:Print(TEXT.ember .. card.kind, left, top, 12 * s, "a")
	if Game and Game.mapName then
		font:Print(TEXT.muted .. string.upper(Game.mapName), x2 - pad, top, 12 * s, "ar")
	end
	top = top - 22 * s

	if card.image then
		local size = IMAGE_SIZE * s
		Rect(left, top - size, left + size, top, COLOR.raised)
		gl.Color(1, 1, 1, 1)
		gl.Texture(":n:" .. card.image)
		gl.TexRect(left, top - size, left + size, top, false, false)
		gl.Texture(false)
		Outline(left, top - size, left + size, top, COLOR.firm, math.max(1, math.floor(s)))
		left = left + size + pad
	end

	local width = (x2 - pad) - left
	if card.title then
		boldFont:Print(TEXT.heading .. card.title, left, top, 20 * s, "a")
		top = top - 28 * s
	end
	local size = (card.kind == "QUOTE") and 18 * s or 16 * s
	local lineHeight = size * 1.35
	local lines = Wrap(font, card.text, width, size, card.title and (MAX_TEXT_LINES - 1) or MAX_TEXT_LINES)
	for i, line in ipairs(lines) do
		font:Print(((card.kind == "QUOTE") and TEXT.heading or TEXT.body) .. line, left, top - (i - 1) * lineHeight, size, "a")
	end
	top = top - #lines * lineHeight
	if card.link then
		font:Print(TEXT.signal .. card.link, left, top - 2 * s, 15 * s, "a")
	end
	if card.author then
		font:Print(TEXT.dimEmber .. card.author, x2 - pad, y1 + pad * 0.6 + 15 * s, 15 * s, "ar")
	end
end

local function DrawBar(x1, y1, x2, y2, s, loadProgress)
	local pad = PAD * s
	local top = y2 - 14 * s

	local message = lastLoadMessage
	if message == "" then
		message = "Loading"
	end
	font:Print(TEXT.muted .. message, x1 + pad, top, 15 * s, "a")
	if loadProgress > 0 then
		boldFont:Print(TEXT.heading .. ("%.0f%%"):format(loadProgress * 100), x2 - pad, top + 3 * s, 20 * s, "ar")
	end

	local barH = math.max(4, math.floor(6 * s))
	local barY1 = math.floor(y1 + 16 * s)
	local barX1, barX2 = x1 + pad, x2 - pad
	Rect(barX1, barY1, barX2, barY1 + barH, COLOR.raised)
	local fill = math.max(0, math.min(1, loadProgress))
	if fill > 0 then
		Rect(barX1, barY1, barX1 + (barX2 - barX1) * fill, barY1 + barH, COLOR.ember)
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

	local width = math.floor(math.min(vsx - 2 * PAD * s, math.max(vsx * PANEL_WIDTH_FRAC, PANEL_MIN_WIDTH * s)))
	local barH = math.floor(BAR_HEIGHT * s)
	local cardH = showTips and math.floor(CARD_HEIGHT * s) or 0
	local x1 = math.floor((vsx - width) * 0.5)
	local x2 = x1 + width
	local y1 = math.floor(vsy * PANEL_BOTTOM_FRAC)
	local y2 = y1 + barH + cardH
	local line = math.max(1, math.floor(s))

	-- the load screen is drawn in 0..1 coordinates; work in pixels instead
	gl.PushMatrix()
	gl.Scale(1 / vsx, 1 / vsy, 1)
	gl.Texture(false)

	Rect(x1, y1, x2, y2, COLOR.panel)
	Outline(x1, y1, x2, y2, COLOR.border, line)
	if showTips then
		Rect(x1 + line, y1 + barH, x2 - line, y1 + barH + line, COLOR.border) -- between the card and the bar
	end
	Brackets(x1, y1, x2, y2, math.floor(11 * s), math.max(2, math.floor(2 * s)))

	if showTips then
		DrawCard(x1, y1 + barH, x2, y2, s)
	end
	DrawBar(x1, y1, x2, y1 + barH, s, loadProgress)

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
