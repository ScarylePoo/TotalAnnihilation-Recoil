-- Weapon definitions (converted from BOTA_CORE_Mines.TDF)

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
		ballistic = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 175,
		edgeeffectiveness = 0.1,
		shakemagnitude = 0,
		shakeduration = 0,
		soundstart = "largegun",
		soundhit = "exmine1",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		damage = {
			default = 200,
			core_t1_def_mine1_armor = 45,
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
		ballistic = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 190,
		edgeeffectiveness = 0.05,
		shakemagnitude = 0,
		shakeduration = 0,
		soundstart = "largegun",
		soundhit = "exmine2",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		damage = {
			default = 400,
			core_t1_def_mine2_armor = 45,
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
		ballistic = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 160,  -- TA 3.1c (was 130)
		edgeeffectiveness = 0.1,
		shakemagnitude = 0,
		shakeduration = 0,
		soundstart = "largegun",
		soundhit = "exmine3",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		damage = {
			default = 700,  -- TA 3.1c (was 1200)
			core_t1_def_mine3_armor = 45,
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
		ballistic = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 140,
		edgeeffectiveness = 0.05,
		shakemagnitude = 0,
		shakeduration = 0,
		soundstart = "largegun",
		soundhit = "exmine4",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		damage = {
			default = 1100,
			core_t1_def_mine4_armor = 45,
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
		ballistic = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 250,
		edgeeffectiveness = 0.1,
		shakemagnitude = 0,
		shakeduration = 0,
		soundstart = "largegun",
		soundhit = "exmine4",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		damage = {
			default = 2000,
			core_t1_def_mine5_armor = 30,
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
		ballistic = 1,
		range = 480,  -- TA 3.1c (was 700)
		reloadtime = 3.6,
		weaponvelocity = 400,
		areaofeffect = 400,  -- TA 3.1c (was 700)
		edgeeffectiveness = 0.15,
		shakemagnitude = 0,
		shakeduration = 0,
		soundstart = "largegun",
		soundhit = "xplonuk3",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		explosiongenerator = "custom:MINI_NUCLEAR_Expl",
		damage = {
			default = 4300,  -- TA 3.1c (was 8000)
			arm_commander_armor = 2900,
			core_commander_armor = 2900,
		},
	},
}
