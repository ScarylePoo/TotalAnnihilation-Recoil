function widget:GetInfo()
	return {
		name    = "Cursor Size",
		desc    = "Picks the HD cursor set (anims/hd/<size>) that suits the screen height",
		author  = "Scary le Poo",
		date    = "2026-11-08",
		license = "GNU GPL, v2 or later",
		layer   = -1000,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
-- TA:Recoil's cursors (tools/cursors/cursors.py) come in 32, 48, 64 and 96 px sets; anims/<cursor>.txt loads the
-- 48 px set by default. This widget swaps every cursor for the set nearest 48 px per 1080 lines of screen
-- (1080p 48, 1440p 64, 4K 96, small windows 32), or the size in the config value "TARCursorSize" if set.
-- The engine itself picks up cursorfight / cursormanfire / cursorwait (Fight, ManualFire, Wait and the waits that
-- fall back to it) before its attack / wait fallbacks. Spring.ReplaceMouseCursor keys on the original file name, so it can swap again when the window is resized.
--------------------------------------------------------------------------------

local SIZES = { 32, 48, 64, 96 }
local CURSORS = {
	"cursornormal", "cursormove", "cursorattack", "cursorattackbad", "cursorfight", "cursormanfire", "cursorselect",
	"cursorpatrol", "cursordefend", "cursorprotect", "cursorrepair", "cursorreclamate", "cursorrevive",
	"cursorcapture", "cursorpickup", "cursorpickupbad", "cursorunload", "cursorunloadbad", "cursorairstrike",
	"cursorsubmerged", "cursorsurfaced", "cursorupgrade", "cursorwait",
}
local current

local function WantedSize()
	local forced = Spring.GetConfigInt("TARCursorSize", 0)
	local want = forced > 0 and forced or select(2, Spring.GetViewGeometry()) / 1080 * 48
	local best, bestD = 48, math.huge
	for _, s in ipairs(SIZES) do
		local d = math.abs(s - want)
		if d < bestD then
			best, bestD = s, d
		end
	end
	return best
end

local function Apply()
	local size = WantedSize()
	if size == current then
		return
	end
	current = size
	local ok = 0
	for _, name in ipairs(CURSORS) do
		if Spring.ReplaceMouseCursor(name, "hd/" .. size .. "/" .. name, name == "cursornormal") then
			ok = ok + 1
		end
	end
	Spring.Echo(string.format("[Cursor Size] %d px cursors (%d of %d in use by the engine swapped)", size, ok, #CURSORS))
end

function widget:Initialize()
	Apply()
end

function widget:ViewResize()
	Apply()
end
