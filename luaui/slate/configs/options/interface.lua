--------------------------------------------------------------------------------
-- Interface tab
--
-- The Slate settings themselves (size, opacity, colour tint, minimap size,
-- the wind and tidal read-outs, broadcasting) read and write through
-- WG.Slate (OPT.slate), which keeps them in the engine config as slate_*
-- variables. Everything else is an engine or widget setting.
--------------------------------------------------------------------------------

local S = OPT.slate

local function SlateGet(key)
	return function() return S.Get(key) end
end

local function SlateSet(key)
	return function(v) S.Set(key, v) end
end

local tintNames = S.TintNames()

return {
	id = "ui", name = "Interface", order = 20,
	options = {
		{ type = "separator", name = "Panels" },
		{ id = "uiscale", name = "Interface size", type = "slider", min = 0.7, max = 1.5, step = 0.05, format = "%.2f", applyOnRelease = true,
		  get = SlateGet("scale"), set = SlateSet("scale"),
		  desc = "Scales every panel of the interface. Panel positions follow.",
		  onSet = function() OPT.rescaleHud() end },
		{ id = "uiopacity", name = "Panel opacity", type = "slider", min = 0.1, max = 1, step = 0.05, format = "%.2f",
		  get = SlateGet("opacity"), set = SlateSet("opacity"),
		  desc = "How solid the panel glass is. Windows with a lot of text never go below 88%." },
		{ id = "uitint", name = "Colour tint", type = "select", options = tintNames, values = tintNames,
		  get = SlateGet("tint"), set = function(idx) S.Set("tint", tintNames[idx] or "None") end,
		  desc = "Leans the panel glass, borders and accent towards a colour. The tints are listed in slate_theme.lua." },
		{ id = "uitintstrength", name = "Tint strength", type = "slider", min = 0, max = 1, step = 0.05, format = "%.2f",
		  get = SlateGet("tintStrength"), set = SlateSet("tintStrength"),
		  showIf = function() return S.Get("tint") ~= "None" end },
		{ id = "minimapsize", name = "Minimap size", type = "slider", min = 0.5, max = 2.5, step = 0.05, format = "%.2f", applyOnRelease = true,
		  get = SlateGet("minimapSize"), set = SlateSet("minimapSize") },
		{ id = "resetlayout", name = "Panel positions", type = "action", label = "Reset to default",
		  set = function() if WG.SlateLayout then WG.SlateLayout.ResetAll() end end,
		  desc = "Puts every panel back where it started. Ctrl+F11 drags panels around." },

		{ type = "separator", name = "Resource bar" },
		{ id = "wind", name = "Wind read-out", type = "bool",
		  get = SlateGet("wind"), set = SlateSet("wind"),
		  desc = "The current wind strength and the map's range, at the right end of the resource bar." },
		{ id = "tidal", name = "Tidal read-out", type = "bool",
		  get = SlateGet("tidal"), set = SlateSet("tidal"),
		  desc = "The map's tidal strength. Only shown on maps with water." },

		{ type = "separator", name = "Players" },
		{ id = "broadcast", name = "Broadcast my camera, FPS and system", type = "bool",
		  get = SlateGet("broadcast"), set = SlateSet("broadcast"),
		  desc = "Lets other players' Slate show your frame rate and system in the players list, and lets spectators follow your camera." },
		{ id = "pausescreen", name = "Pause overlay", type = "bool", widget = "Slate Pause Screen", requires = "Slate Pause Screen" },
		{ id = "simpleminimapcolors", name = "Simple minimap colours", type = "bool", config = "SimpleMiniMapColors", cmd = "minimap simplecolors %d",
		  desc = "Green is you, blue is allied, red is enemy." },

		{ type = "separator", name = "Camera" },
		{ id = "edgescroll", name = "Scroll at the screen edge", type = "bool", config = "WindowedEdgeMove", cmd = "edgemove %d" },
		{ id = "scrollspeed", name = "Scroll speed", type = "slider", min = 1, max = 100, step = 1, config = "ScrollWheelSpeed", configType = "int",
		  desc = "Mouse wheel zoom speed. Negative values in the config invert it." },
	},
}
