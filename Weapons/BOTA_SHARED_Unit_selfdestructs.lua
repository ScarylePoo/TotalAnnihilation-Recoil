-- Weapon definitions (converted from BOTA_SHARED_Unit_selfdestructs.TDF)

return {
	small_unit = {
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
		areaofeffect = 75,
		soundstart = "largegun",
		soundhit = "xplomed2",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		shakemagnitude = 0,
		shakeduration = 0,
		damage = {
			default = 200,
		},
	},
	medium_unit = {
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
		areaofeffect = 95,
		soundstart = "largegun",
		soundhit = "xplolrg3",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom2",
		shakemagnitude = 0,
		shakeduration = 0,
		damage = {
			default = 250,
		},
	},
	big_unit = {
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
			default = 350,
		},
	},
	crawl_blastsml = {
		-- TA 3.1c weapon crawl_blastsml (BOTA used big_unit for it as well)
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
		areaofeffect = 275,  -- TA 3.1c (was 110)
		soundstart = "largegun",
		soundhit = "xplolrg3",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom2",
		shakemagnitude = 8,
		shakeduration = .3,
		damage = {
			default = 1200,  -- TA 3.1c (was 350)
		},
	},
	crawl_blast = {
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
		areaofeffect = 556,
		soundstart = "largegun",
		soundhit = "xplonuk3",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom2",
		shakemagnitude = 24,
		shakeduration = 1.5,
		damage = {
			default = 2500,
		},
	},
	corpyro_suicide = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		ballistic = 1,
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 325,
		soundstart = "largegun",
		soundhit = "xplomed1",
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		shakemagnitude = 0,
		shakeduration = 0,
		damage = {
			default = 1400,
		},
	},
}
