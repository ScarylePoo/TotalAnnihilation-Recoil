-- Weapon definitions (native Recoil tags; converted from BOTA_SHARED_Building_selfdestructs.TDF)

return {
	small_building = {
		-- used by units
		-- ARM_T1_ECO_MetalExtractor
		-- ARM_T2_ECO_MohoMine
		-- CORE_T1_ECO_MetalExtractor
		-- CORE_T2_ECO_MohoMine
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
		areaofeffect = 205,
		craterareaofeffect = 307.5,
		soundstart = "largegun",
		soundhit = "xplosml3",
		explosiongenerator = "custom:SMALL_UNIT_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		damage = {
			default = 900,
		},
	},
	medium_building = {
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
		explosiongenerator = "custom:BIG_UNIT_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		damage = {
			default = 1400,
		},
	},
	large_building = {
		-- used by units
		-- ARM_T2_ECO_MohoMetalMaker
		-- CORE_T2_ECO_MohoMetalMaker
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
		areaofeffect = 400,
		craterareaofeffect = 600,
		soundstart = "largegun",
		soundhit = "xplolrg4",
		explosiongenerator = "custom:FACTORY_Expl",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		damage = {
			default = 1800,
		},
	},
	estor_building = {
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
		areaofeffect = 420,
		craterareaofeffect = 630,
		soundstart = "largegun",
		soundhit = "xplonuk1",
		explosiongenerator = "custom:ATOMIC_BLASTSML",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		damage = {
			default = 1900,
		},
	},
	atomic_blast = {
		-- used by units
		-- type
		turret = 1,
		-- visuals
		-- sounds
		soundstart = "largegun",
		soundhit = "xplonuk3",
		-- behaviour
		weaponvelocity = 250,
		-- stats
		range = 480,
		reloadtime = 3.6,
		areaofeffect = 516,
		craterareaofeffect = 774,
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		damage = {
			default = 2000,
		},
	},
}
