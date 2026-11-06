-- Weapon definitions (converted from BOTA_ARM_Mines.TDF)

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
		ballistic = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 160,
		edgeeffectiveness = 0.1,
		shakemagnitude = 0,
		shakeduration = 0,
		soundstart = "largegun",
		soundhit = "exmine1",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom2",
		damage = {
			default = 400,
			arm_t1_def_mine1_armor = 30,
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
		ballistic = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 200,
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
			default = 600,
			arm_t1_def_mine2_armor = 30,
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
		ballistic = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 130,
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
			default = 1300,  -- TA 3.1c (was 1200)
			arm_t1_def_mine3_armor = 30,
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
		ballistic = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 180,
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
			default = 1500,
			arm_t1_def_mine4_armor = 30,
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
		ballistic = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 130,  -- TA 3.1c (was 150)
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
			default = 2000,  -- TA 3.1c (was 4000)
			arm_t1_def_mine5_armor = 30,
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
		ballistic = 1,
		range = 480,  -- TA 3.1c (was 700)
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 350,  -- TA 3.1c (was 700)
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
			default = 4500,  -- TA 3.1c (was 9000)
			arm_commander_armor = 2900,
			core_commander_armor = 2900,
		},
	},
}
