-- Weapon definitions (converted from BOTA_SHARED_Unit_explosions.TDF)

return {
	small_unitex = {
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
		areaofeffect = 30,
		soundstart = "largegun",
		soundhit = "xplomed2",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		shakemagnitude = 0,
		shakeduration = 0,
		damage = {
			default = 30,
		},
	},
	big_unitex = {
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
		areaofeffect = 110,
		soundstart = "largegun",
		soundhit = "xplolrg3",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom2",
		shakemagnitude = 8,
		shakeduration = .3,
		damage = {
			default = 50,
		},
	},
	corpyro_blast = {
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
		areaofeffect = 128,
		soundstart = "largegun",
		soundhit = "xplolrg3",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom2",
		shakemagnitude = 0,
		shakeduration = 0,
		damage = {
			default = 60,
			core_t2_bot_pyro_armor = 15,
		},
	},
	decoy_commander_blast = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		rendertype = 4,
		avoidfriendly = 0,
		collidefriendly = 0,
		ballistic = 1,
		turret = 1,
		range = 380,
		reloadtime = 3.6,
		weaponvelocity = 250,
		soundstart = "largegun",
		soundhit = "xplonuk4",
		explosiongaf = "commboom",
		explosionart = "commboom",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom2",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplashlg",
		shakemagnitude = 32,
		shakeduration = 2,
		areaofeffect = 950,
		edgeeffectiveness = 0.15,
		damage = {
			default = 100,
		},
	},
}
