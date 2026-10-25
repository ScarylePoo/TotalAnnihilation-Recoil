--------------------------------------------------------------------------------
-- Slate theme
--
-- The look itself lives in luaui/slate/rml/theme.rcss (and the <style> block
-- of each document). This file holds what the player can change in the
-- settings, with its defaults, plus the few colours those settings are
-- computed from: a colour tint mixes the panel glass, borders and accent
-- towards the chosen colour, so those three are kept here too and must match
-- the values in theme.rcss.
--
-- Colours are {r, g, b, a} in 0-1. Sizes are in dp (pixels at 1920x1080).
--------------------------------------------------------------------------------

return {
	-- Panel glass. `opacity` is the alpha of the panel body (0 = invisible,
	-- 1 = solid). Players change it in the settings or with "/slate opacity 0.6".
	opacity      = 0.60,
	-- Tell other players' Slate your frame rate, system and camera position
	-- (FPS column, system details and click-to-follow in the players list).
	broadcast    = true,
	-- Overall size multiplier on top of resolution scaling.
	scale        = 1.0,
	-- Minimap size multiplier. Players change it in the settings screen.
	minimapSize  = 1.0,

	-- Colour tint. `tint` names one of the entries in `tints`; `tintStrength`
	-- (0-1) is how far the panel glass, borders and accent lean towards it.
	-- Players pick both in the settings screen or with "/slate tint Blue".
	tint         = "None",
	tintStrength = 0.5,
	tints = {
		{ name = "None" },
		{ name = "Blue",   color = { 0.20, 0.45, 0.95 } },
		{ name = "Teal",   color = { 0.10, 0.70, 0.65 } },
		{ name = "Green",  color = { 0.25, 0.72, 0.30 } },
		{ name = "Amber",  color = { 0.95, 0.62, 0.15 } },
		{ name = "Red",    color = { 0.90, 0.25, 0.22 } },
		{ name = "Pink",   color = { 0.95, 0.40, 0.70 } },
		{ name = "Purple", color = { 0.58, 0.36, 0.92 } },
	},

	-- The untinted colours (must match theme.rcss)
	panel        = { 0.050, 0.055, 0.063 },          -- body colour (alpha = opacity)
	border       = { 1.00, 1.00, 1.00, 0.14 },
	accent       = { 0.663, 0.741, 0.816, 1.0 },      -- headings, active filter, state pips

	margin       = 16,                                -- gap from the screen edge, dp
	gap          = 16,                                -- gap between stacked panels, dp
}
