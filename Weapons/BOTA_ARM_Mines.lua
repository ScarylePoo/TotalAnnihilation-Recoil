-- Weapon definitions (native Recoil tags; converted from BOTA_ARM_Mines.TDF)

return {
	armmine1 = {
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
		areaofeffect = 160,
		craterareaofeffect = 240,
		edgeeffectiveness = 0.1,
		soundstart = "largegun",
		soundhit = "exmine1",
		damage = {
			default = 400,
		},
	},
	armmine2 = {
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
		areaofeffect = 200,
		craterareaofeffect = 300,
		edgeeffectiveness = 0.05,
		soundstart = "largegun",
		soundhit = "exmine2",
		damage = {
			default = 600,
		},
	},
	armmine3 = {
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
	armmine4 = {
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
		areaofeffect = 180,
		craterareaofeffect = 270,
		edgeeffectiveness = 0.05,
		soundstart = "largegun",
		soundhit = "exmine4",
		damage = {
			default = 1500,
		},
	},
	armmine5 = {
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
		areaofeffect = 150,
		craterareaofeffect = 225,
		edgeeffectiveness = 0.1,
		soundstart = "largegun",
		soundhit = "exmine4",
		damage = {
			default = 4000,
		},
	},
	armmine6 = {
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
		weaponvelocity = 250,
		areaofeffect = 700,
		craterareaofeffect = 1050,
		edgeeffectiveness = 0.15,
		soundstart = "largegun",
		soundhit = "xplonuk3",
		explosiongenerator = "custom:MINI_NUCLEAR_Expl",
		damage = {
			default = 9000,
		},
	},
}
