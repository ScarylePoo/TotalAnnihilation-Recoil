function widget:GetInfo()
	return {
		name    = "Set Target Key",
		desc    = "Binds Y to Set Target (unit_target_on_the_move.lua), as Splinter Faction does",
		author  = "Scary le Poo",
		date    = "2026-11-08",
		license = "GNU GPL, v2 or later",
		layer   = 0,
		enabled = true,
	}
end

-- Only if the player hasn't put something else on Y; re-applied after Slate Keybindings reloads the binds.
local function Bind()
	local binds = Spring.GetKeyBindings("y") or {}
	for _, b in ipairs(binds) do
		local action = b.command or b[1]
		if action and action ~= "settarget" then
			return
		end
	end
	Spring.SendCommands("bind y settarget")
end

function widget:Initialize()
	Bind()
	if WG.SlateKeybindings and WG.SlateKeybindings.AddReapplyHook then
		WG.SlateKeybindings.AddReapplyHook("SetTargetKey", Bind)
	end
end

function widget:Shutdown()
	if WG.SlateKeybindings and WG.SlateKeybindings.RemoveReapplyHook then
		WG.SlateKeybindings.RemoveReapplyHook("SetTargetKey")
	end
end
