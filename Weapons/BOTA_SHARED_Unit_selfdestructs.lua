-- Weapon definitions (native Recoil tags; converted from BOTA_SHARED_Unit_selfdestructs.TDF)

return {
	small_unit = {
		-- used by units
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 75,
		craterareaofeffect = 112.5,
		soundstart = "largegun",
		soundhit = "xplomed2",
		explosiongenerator = "custom:SMALL_SUICIDE_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
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
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 95,
		craterareaofeffect = 142.5,
		soundstart = "largegun",
		soundhit = "xplolrg3",
		explosiongenerator = "custom:MED_SUICIDE_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
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
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 110,
		craterareaofeffect = 165,
		soundstart = "largegun",
		soundhit = "xplolrg3",
		explosiongenerator = "custom:BIG_SUICIDE_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		damage = {
			default = 350,
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
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 556,
		craterareaofeffect = 834,
		soundstart = "largegun",
		soundhit = "xplonuk3",
		explosiongenerator = "custom:CRAWL_SUICIDE_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
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
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 325,
		craterareaofeffect = 487.5,
		soundstart = "largegun",
		soundhit = "xplomed1",
		explosiongenerator = "custom:PYRO_SUICIDE_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		damage = {
			default = 1400,
		},
	},
}
