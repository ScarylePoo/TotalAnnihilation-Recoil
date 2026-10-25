-- Weapon definitions (native Recoil tags; converted from BOTA_CORE_Mines.TDF)

return {
	cormine1 = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		name = "Level 1 Mine",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 175,
		craterareaofeffect = 262.5,
		edgeeffectiveness = 0.1,
		soundstart = "largegun",
		soundhit = "exmine1",
		damage = {
			default = 200,
		},
	},
	cormine2 = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		name = "Blast Mine",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 190,
		craterareaofeffect = 285,
		edgeeffectiveness = 0.05,
		soundstart = "largegun",
		soundhit = "exmine2",
		damage = {
			default = 400,
		},
	},
	cormine3 = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		name = "Focal Mine",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 130,
		craterareaofeffect = 195,
		edgeeffectiveness = 0.1,
		soundstart = "largegun",
		soundhit = "exmine3",
		damage = {
			default = 1200,
		},
	},
	cormine4 = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		name = "Wide Blast Mine",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 140,
		craterareaofeffect = 210,
		edgeeffectiveness = 0.05,
		soundstart = "largegun",
		soundhit = "exmine4",
		damage = {
			default = 1100,
		},
	},
	cormine5 = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		name = "Whap Mine",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 250,
		craterareaofeffect = 375,
		edgeeffectiveness = 0.1,
		soundstart = "largegun",
		soundhit = "exmine4",
		damage = {
			default = 2000,
		},
	},
	cormine6 = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		name = "Nuclear Mine",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		range = 700,
		reloadtime = 3.6,
		weaponvelocity = 400,
		areaofeffect = 700,
		craterareaofeffect = 1050,
		edgeeffectiveness = 0.15,
		soundstart = "largegun",
		soundhit = "xplonuk3",
		explosiongenerator = "custom:MINI_NUCLEAR_Expl",
		damage = {
			default = 8000,
		},
	},
}
