--------------------------------------------------------------------------------
-- TA:Recoil loading screen: what it plays and what it shows (LuaIntro/Addons/main.lua, music.lua).
--
-- Each load shows one card above the progress bar, a different one each time (the cards take turns: a tip, then a
-- quote or a unit note). To add one, add an entry to a list below:
--
--   tips   { title = "...", text = "...", image = "path/in/game.png" (optional), link = "..." (optional) }
--   units  { title = "...", text = "...", image = "unitpics/XXX.png" }
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

	units = {
		{ image = "unitpics/ARM_Commander.png", title = "Arm Commander",
		  text = "The heart of every Arm war effort. It builds, it repairs, and its D-Gun erases whatever it touches. Lose it and the war is lost." },
		{ image = "unitpics/CORE_Commander.png", title = "Core Commander",
		  text = "Core's commander: a builder, a fighter, and the last thing standing between the Core and defeat. Guard it well." },
		{ image = "unitpics/CORE_T3_BOT_Krogoth.png", title = "Krogoth",
		  text = "Core's experimental Kbot. Slow, enormous and nearly unstoppable once it reaches the front." },
		{ image = "unitpics/ARM_T2_DEF_BigBertha.png", title = "Big Bertha",
		  text = "Arm's long range plasma cannon. It shells targets from across the map." },
		{ image = "unitpics/CORE_T2_DEF_Intimidator.png", title = "Intimidator",
		  text = "Core's answer to the Big Bertha: a long range cannon that turns distant bases into craters." },
		{ image = "unitpics/ARM_T2_DEF_Annihilator.png", title = "Annihilator",
		  text = "A heavy energy weapon that cuts down anything that comes near. It needs a lot of power to fire." },
		{ image = "unitpics/CORE_T2_DEF_DoomsdayMachine.png", title = "Doomsday Machine",
		  text = "Core's fortress: several heavy weapons in one armoured shell that closes up when it is not firing." },
		{ image = "unitpics/ARM_T2_BOT_Zeus.png", title = "Zeus",
		  text = "An Arm assault Kbot with a short-ranged lightning gun that tears through armour." },
		{ image = "unitpics/CORE_T2_BOT_Pyro.png", title = "Pyro",
		  text = "A fast Core Kbot with a flamethrower. Deadly up close, and when it dies it takes the ground around it with it." },
		{ image = "unitpics/ARM_T1_VEH_Flash.png", title = "Flash",
		  text = "A cheap, fast Arm tank with a rapid-fire cannon. Good for raiding and early harassment." },
		{ image = "unitpics/CORE_T1_BOT_Ak.png", title = "A.K.",
		  text = "Core's basic infantry Kbot. Cheap and quick to build, dangerous in numbers." },
	},

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
