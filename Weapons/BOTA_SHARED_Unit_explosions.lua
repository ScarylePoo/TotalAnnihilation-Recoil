-- Weapon definitions (native Recoil tags; converted from BOTA_SHARED_Unit_explosions.TDF)

return {
	small_unitex = {
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
		areaofeffect = 30,
		craterareaofeffect = 45,
		soundstart = "largegun",
		soundhit = "xplomed2",
		explosiongenerator = "custom:SMALL_UNIT_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
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
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 110,
		craterareaofeffect = 165,
		soundstart = "largegun",
		soundhit = "xplolrg3",
		explosiongenerator = "custom:BIG_UNIT_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
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
		turret = 1,
		range = 550,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 110,
		craterareaofeffect = 165,
		soundstart = "largegun",
		soundhit = "xplolrg3",
		explosiongenerator = "custom:HUGE_UNIT_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
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
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 128,
		craterareaofeffect = 192,
		soundstart = "largegun",
		soundhit = "xplolrg3",
		explosiongenerator = "custom:PYRO_UNIT_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
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
		turret = 1,
		range = 480,
		reloadtime = 3.6,
		weaponvelocity = 250,
		areaofeffect = 275,
		craterareaofeffect = 412.5,
		soundstart = "largegun",
		soundhit = "xplonuk3",
		explosiongenerator = "custom:CRAWL_UNIT_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
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
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 380,
		reloadtime = 3.6,
		weaponvelocity = 250,
		soundstart = "largegun",
		soundhit = "xplonuk4",
		areaofeffect = 950,
		craterareaofeffect = 1425,
		edgeeffectiveness = 0.15,
		explosiongenerator = "custom:LRPC_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		damage = {
			default = 100,
		},
	},
}
