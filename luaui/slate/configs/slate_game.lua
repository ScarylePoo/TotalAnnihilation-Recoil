--------------------------------------------------------------------------------
-- Slate game config
--
-- Everything Slate needs to know about the game it is running in. The panel
-- widgets read only this table, so adopting Slate in another Total
-- Annihilation style game means copying the luaui/slate/ folder plus the two
-- slate_*.lua config files, then editing this one.
--------------------------------------------------------------------------------

-- Build menu filters go by the unit's own customparams.buildcategory ("economy", "defense", "factory", or for mobile units "scout", "skirmish", "support" or "utility"),
-- set in every file under units/. To move a unit to another filter, change it there.
local function InCategory(name)
	return function(ud)
		return ud.customParams and ud.customParams.buildcategory == name
	end
end

return {
	-- Resources shown in the resource bar, left to right. `key` is the engine
	-- resource name passed to Spring.GetTeamResources; `icon` a file in
	-- luaui/slate/images/ (premultiplied alpha, see theme.rcss) or nil.
	resources = {
		{ key = "metal",  label = "Metal",  color = "#c9d3de", icon = "metal.png" },
		{ key = "energy", label = "Energy", color = "#f2d45c", icon = "energy.png" },
	},

	-- Optional read-outs at the right end of the resource bar. Players toggle
	-- them in the settings or with "/slate wind" and "/slate tidal". Tidal
	-- hides itself on maps without water.
	addons = {
		wind  = true,
		tidal = true,
	},

	-- Build menu. Filters are offered only when the current builder has at
	-- least one matching entry; "All" is always first.
	buildColumns = 4,
	buildRows    = 5,
	buildCategories = {
		{ label = "Economy",   match = InCategory("economy") },
		{ label = "Defence",   match = InCategory("defense") },
		{ label = "Factories", match = InCategory("factory") },
		-- what factories build (the roles Splinter Faction's build menu uses)
		{ label = "Scout",     match = InCategory("scout") },
		{ label = "Skirmish",  match = InCategory("skirmish") },
		{ label = "Support",   match = InCategory("support") },
		{ label = "Utility",   match = InCategory("utility") },
	},
	-- Picture for a build tile or the selection panel: a file path. Leave nil
	-- to use the engine's build picture (unitpics/<name>.<ext>).
	unitPicturePath = nil,

	-- Commands never shown in the order grid (matched against the command's
	-- action name). The engine still accepts them from hotkeys.
	hiddenCommands = {
		timewait = true, deathwait = true, squadwait = true, gatherwait = true,
		loadonto = true, selfd = true,
	},
	orderColumns = 5,
	stateColumns = 4,

	-- Stat cells in the selection panel for a single unit. Each entry returns a
	-- string, or nil to leave the cell out. `res` is { metalMake, metalUse,
	-- energyMake, energyUse } for a live unit, nil for a build-menu preview.
	unitStats = {
		{ label = "Metal",  value = function(ud, res)
			if res then return string.format("%+.1f", res[1] - res[2]) end
			return string.format("%d", ud.metalCost)
		end },
		{ label = "Energy", value = function(ud, res)
			if res then return string.format("%+.0f", res[3] - res[4]) end
			return string.format("%d", ud.energyCost)
		end },
		{ label = "Build power", value = function(ud)
			if (ud.buildSpeed or 0) > 0 then return string.format("%d", ud.buildSpeed) end
		end },
		{ label = "Speed", value = function(ud)
			if (ud.speed or 0) > 0 then return string.format("%d", ud.speed) end
		end },
		{ label = "Range", value = function(ud)
			if (ud.maxWeaponRange or 0) > 0 then return string.format("%d", ud.maxWeaponRange) end
		end },
	},

	-- Start each game in line-of-sight view (the L key view that shades what
	-- you cannot see). Players can still switch it off.
	losView = true,

	-- Interface sounds, as names or paths for Spring.PlaySoundFile. Leave an
	-- entry nil for silence. click/hover are the buttons; the chat entries
	-- are incoming chat by channel.
	sounds = {
		click    = "luaui/sounds/buildbar_click.wav",
		hover    = nil,
		chat     = "luaui/sounds/message_admin.wav",
		allychat = "luaui/sounds/message_team.wav",
		specchat = nil,
		whisper  = "luaui/sounds/message_private.wav",
	},

	-- The faction chooser at the start of a game (slate_factionchooser.lua),
	-- one card per faction. `id` is the commander the spawn gadget creates
	-- (gamedata/sidedata.lua); `picture` a file path from the game root, shown
	-- at 392x220 dp (1568x880 pixels, so it is sharp up to 8K); `color` tints
	-- the card. The pictures and the emblems beside them (<faction>_emblem.png,
	-- transparent, premultiplied) are drawn by tools/faction_logos.py.
	factions = {
		{
			id      = "arm_commander",
			name    = "Arm",
			blurb   = "The free individuals of the Arm refuse the Core's patterning of minds into machines. "
				.. "Their machines are lighter, quicker and cheaper: they win by speed, range and numbers.",
			picture = "luaui/slate/images/factions/arm.png",
			color   = "#4a86e0",
		},
		{
			id      = "core_commander",
			name    = "Core",
			blurb   = "The Core would copy every human mind into a machine, and has fought four thousand years to do it. "
				.. "Their machines are heavier, tougher and hit harder.",
			picture = "luaui/slate/images/factions/core.png",
			color   = "#d84a3c",
		},
	},

	-- Extra entries in the game menu, after Slate's own (settings, graphs,
	-- share, log, key bindings, widgets). `command` goes to Spring.SendCommands;
	-- `confirm` asks for a second click; `playersOnly` hides the entry from
	-- spectators.
	menu = {},
}
