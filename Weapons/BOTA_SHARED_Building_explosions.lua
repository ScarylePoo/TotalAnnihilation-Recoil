-- Weapon definitions (converted from BOTA_SHARED_Building_explosions.TDF)

return {
	small_buildingex = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 70,
		areaofeffect = 205,
		soundstart = "largegun",
		soundhit = "xplosml3",
		explosiongenerator = "custom:SMALL_SUICIDE_Expl",
		damage = {
			default = 40,
		},
	},
	medium_buildingex = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 105,
		soundstart = "largegun",
		soundhit = "xplomed1",
		explosiongenerator = "custom:MED_SUICIDE_Expl",
		shakemagnitude = 0,
		shakeduration = 0,
		damage = {
			default = 100,
		},
	},
	large_buildingex = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 120,
		soundstart = "largegun",
		soundhit = "xplolrg4",
		explosiongenerator = "custom:FACTORY_Expl",
		shakemagnitude = 8,
		shakeduration = .3,
		damage = {
			default = 300,
		},
	},
	estor_buildingex = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		rendertype = 4,
		ballistic = 1,
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 150,
		soundstart = "largegun",
		soundhit = "xplonuk1",
		explosiongenerator = "custom:ESTORBUILDING_Expl",
		shakemagnitude = 8,
		shakeduration = .5,
		damage = {
			default = 900,
		},
	},
	atomic_blastex = {
		-- used by units
		-- type
		rendertype = 4,
		turret = 1,
		ballistic = 1,
		-- visuals
		-- sounds
		soundstart = "largegun",
		soundhit = "xplonuk3",
		-- behaviour
		weaponvelocity = 250,
		-- stats
		range = 480,
		reloadtime = 3.6,
		areaofeffect = 260,
		damage = {
			default = 1000,
		},
	},
}
