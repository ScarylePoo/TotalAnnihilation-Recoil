--------------------------------------------------------------------------------
-- TA:Recoil loading screen: what it plays and what it shows (LuaIntro/Addons/main.lua, music.lua).
--
-- Each load shows one card above the progress bar, a different one each time (the cards take turns: a tip, then a
-- quote or a unit note). To add one, add an entry to a list below:
--
--   tips   { title = "...", text = "...", image = "path/in/game.png" (optional), link = "..." (optional) }
--   units  { title = "...", text = "...", image = "unitpics/XXX.png" }   (in loadscreen_units.lua)
--   quotes { "the quote", "who said it" }
--
-- image is any picture inside the game (png, jpg or dds), shown square beside the text; "\n" in text starts a new
-- line. Up to about four lines of text fit. Background pictures are the files in bitmaps/loadpictures/ (one is
-- picked at random each load; any size, cropped to fill the screen).
--------------------------------------------------------------------------------

return {
	-- the track played while loading; the in-game music player carries on with it, then picks the next song
	music = "music/Total Annihilation OST/Intro.ogg",

	tips = {
		{ title = "Metal spots",
		  text = "Metal Extractors only go on metal spots. Press F4 to light up every spot on the map, or right-click one with a builder selected to queue a mex there. Drag the right-click across several spots to queue them all." },
		{ title = "Moho Mines",
		  text = "Build a Moho Mine right on top of your Metal Extractor: the mex keeps producing while the moho goes up, then makes way for it. A moho makes three times the metal." },
		{ title = "Geothermal vents",
		  text = "Right-click a geothermal vent with a builder selected to queue a Geothermal Powerplant on it. Vents are marked with a yellow column." },
		{ title = "Set Target",
		  text = "Press Y and click an enemy: your units keep moving where you send them but fire at that target whenever it is in range. Ctrl+Y cancels it." },
		{ title = "Splitting your army",
		  text = "Alt+S splits the selected units into two halves, Alt+D swaps to the other half, and Alt+X puts them back together." },
		{ title = "Control groups",
		  text = "Ctrl+number makes a control group, the number selects it, and a quick double press centres the camera on it.\nAlt+number makes every new unit of the selected types join that group." },
		{ title = "Formations",
		  text = "Hold the right mouse button and drag to draw a line: your units spread out along it. A plain click moves a group into a line abreast facing the way it is going." },
		{ title = "Jumping the queue",
		  text = "Hold Space while giving an order to put it at the front of the queue. Space+Shift slips it in wherever it fits best along the way." },
		{ title = "Construction priority",
		  text = "Set a builder or factory to High priority and it gets resources first when you run short. Low priority work only uses what is left over." },
		{ title = "Press Enter to chat",
		  text = "Ctrl+Enter switches to All Chat\nAlt+Enter switches to Ally Chat\nShift+Enter switches to Spectator Chat" },
		{ title = "Keybinds",
		  text = "Every key can be changed in the Keybinds window. Hover a build or order button and press Ctrl+Insert to bind it to a key, Ctrl+Delete to unbind." },
	},

	-- unit notes: LuaIntro/Configs/loadscreen_units.lua
	units = VFS.Include("LuaIntro/Configs/loadscreen_units.lua"),

	quotes = {
		{ "Strategy without tactics is the slowest route to victory. Tactics without strategy is the noise before defeat.", "Sun Tzu" },
		{ "He will win who knows when to fight and when not to fight.", "Sun Tzu" },
		{ "When I have won a victory I do not repeat my tactics but respond to circumstances in an infinite variety of ways.", "Sun Tzu" },
		{ "The art of war is the art of deception.", "Sun Tzu" },
		{ "The best defense is a confusing offense.", "Kimberly Pauley" },
		{ "When your opponent is making a mistake, do nothing to interfere.", "Napoleon Bonaparte" },
		{ "No campaign plan survives first contact with the enemy.", "Carl von Clausewitz" },
		{ "Tactics is the art of using troops in battle; strategy is the art of using battles to win the war.", "Carl von Clausewitz" },
		{ "The enemy of a good plan is the dream of a perfect plan.", "Carl von Clausewitz" },
		{ "The best form of defense is attack.", "Carl von Clausewitz" },
	},
}
