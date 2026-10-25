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
		explosiongenerator = "custom:SMALL_UNIT_Expl",
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
		explosiongenerator = "custom:BIG_UNIT_Expl",
		damage = {
			default = 50,
		},
	},
	huge_unitex = {
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
		range = 550,
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
		explosiongenerator = "custom:HUGE_UNIT_Expl",
		damage = {
			default = 700,
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
		explosiongenerator = "custom:PYRO_UNIT_Expl",
		damage = {
			default = 60,
		},
	},
	crawl_blastex = {
		-- used by units
		-- ARM_T1_ECO_MetalMaker
		-- CORE_T1_ECO_MetalMaker
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
		areaofeffect = 275,
		soundstart = "largegun",
		soundhit = "xplonuk3",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom2",
		shakemagnitude = 24,
		shakeduration = 1.5,
		explosiongenerator = "custom:CRAWL_UNIT_Expl",
		damage = {
			default = 1200,
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
		explosiongenerator = "custom:LRPC_Expl",
		damage = {
			default = 100,
		},
	},
}
