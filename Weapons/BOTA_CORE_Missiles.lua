-- Weapon definitions (converted from BOTA_CORE_Missiles.TDF)

return {
	corvtol_missile = {
		-- used by units
		-- CORE_T1_AIR_Avenger
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 109,
		name = "Guided Missiles",
		rendertype = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		lineofsight = 1,
		model = "missile",
		range = 502,  -- TA 3.1c (was 620)  -- 502
		reloadtime = 3,  -- TA 3.1c (was 5)  -- 3
		weapontimer = 5,
		weaponvelocity = 470,
		startvelocity = 425,
		weaponacceleration = 149,
		turnrate = 16384,
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "Rocklit3",
		soundhit = "xplosml2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 8000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 46,  -- TA 3.1c (was 136)
			arm_aircraft = 136,
			core_aircraft = 136,
		},
	},
	corkbot_missile = {
		-- used by units
		-- CORE_T1_BOT_Crasher
		-- CORE_T1_SEA_Searcher
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 101,
		name = "Missiles",
		rendertype = 1,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 590,  -- TA 3.1c (was 800)  -- 590//690
		reloadtime = 2.5,  -- 2.5
		weapontimer = 5,
		weaponvelocity = 650,
		startvelocity = 450,
		weaponacceleration = 104,
		turnrate = 33000,  -- TA 3.1c (was 17000)  -- 33000
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "rocklit1",
		soundhit = "xplosml2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 9000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 32,  -- TA 3.1c (was 43)  -- 32
			arm_aircraft = 80,
			core_aircraft = 80,
		},
	},
	corrl_missile = {
		-- used by units
		-- CORE_T1_DEF_Pulverizer
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 107,
		name = "Missiles",
		rendertype = 1,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 700,  -- TA 3.1c (was 820)
		reloadtime = 2,
		weapontimer = 5,
		weaponvelocity = 650,
		startvelocity = 460,
		weaponacceleration = 152,
		turnrate = 50000,  -- TA 3.1c (was 20000)
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "rockhvy2",
		soundhit = "xplomed2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 10000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 45,  -- TA 3.1c (was 67)
			arm_aircraft = 95,
			core_aircraft = 95,
		},
	},
	corah_weapon = {
		-- used by units
		-- CORE_T1_HOV_Slinger
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 199,
		name = "Missiles",
		rendertype = 1,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 600,  -- TA 3.1c (was 820)
		reloadtime = 2,
		weapontimer = 5,
		weaponvelocity = 660,
		startvelocity = 470,
		weaponacceleration = 154,
		turnrate = 50000,
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "rockhvy2",
		soundhit = "xplomed2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 10000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 46,
			arm_aircraft = 97,
			core_aircraft = 97,
		},
	},
	corfrt_missile = {
		-- used by units
		-- CORE_T1_SEADEF_Stinger
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 148,
		name = "Missiles",
		rendertype = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		lineofsight = 1,
		turret = 1,
		model = "missile",
		range = 700,
		reloadtime = 2,
		weapontimer = 5,
		weaponvelocity = 660,
		startvelocity = 460,
		weaponacceleration = 152,
		turnrate = 50000,
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "rockhvy2",
		soundhit = "xplomed2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 10000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 45,
			arm_aircraft = 95,
			core_aircraft = 95,
		},
	},
	corseap_weapon3 = {
		-- used by units
		-- CORE_T1_SEAPL_Typhoon
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 98,
		name = "Guided Missiles",
		rendertype = 1,
		lineofsight = 1,
		model = "missile",
		range = 510,  -- TA 3.1c (was 610)  -- 510
		reloadtime = 3,
		weapontimer = 5,
		weaponvelocity = 480,
		startvelocity = 420,
		weaponacceleration = 146,
		turnrate = 16384,
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "Rocklit3",
		soundhit = "xplosml2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 8000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 44,
			arm_aircraft = 130,
			core_aircraft = 130,
		},
	},
	core_seaplane_fighter_missile = {
		-- used by units
		-- CORE_T1_SEAPL_Voodoo
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 76,
		name = "Guided Missiles",
		rendertype = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		lineofsight = 1,
		model = "missile",
		range = 510,
		reloadtime = 3,
		weapontimer = 6,
		weaponvelocity = 522,
		startvelocity = 420,
		weaponacceleration = 146,
		turnrate = 19384,
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "Rocklit3",
		soundhit = "xplosml2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 8000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 50,
			arm_aircraft = 140,
			core_aircraft = 140,
		},
	},
	cortruck_missile = {
		-- used by units
		-- CORE_T1_VEH_Slasher
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 105,
		name = "Missiles",
		rendertype = 1,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 600,  -- TA 3.1c (was 800)  -- 600
		reloadtime = 2.5,
		weapontimer = 5,
		weaponvelocity = 545,
		startvelocity = 450,
		weaponacceleration = 136,
		turnrate = 30000,  -- TA 3.1c (was 15000)  -- 30000
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "rockhvy2",
		soundhit = "xplomed2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 8000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 41,  -- TA 3.1c (was 53)  -- 41//61
			arm_aircraft = 92,
			core_aircraft = 92,
		},
	},
	corvtol_advmissile2 = {
		-- TA 3.1c weapon corvtol_advmissile2 (BOTA used core_stealth_fighter_missile for it as well)
		-- used by units
		-- CORE_T2_AIR_Vamp
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 113,
		name = "Guided Missiles",
		rendertype = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		lineofsight = 1,
		model = "missile",
		range = 650,
		reloadtime = 3,
		weapontimer = 7,
		weaponvelocity = 550,
		startvelocity = 450,
		weaponacceleration = 131,
		turnrate = 24384,
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "Rocklit3",
		soundhit = "xplosml2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 8000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 68,
			arm_aircraft = 155,
			core_aircraft = 155,
		},
	},
	corvtol_advmissile = {
		-- TA 3.1c weapon corvtol_advmissile (BOTA used core_stealth_fighter_missile for it as well)
		-- used by units
		-- CORE_T2_AIR_Vamp
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 113,
		name = "Guided Missiles",
		rendertype = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		lineofsight = 1,
		model = "missile",
		range = 650,
		reloadtime = 3,
		weapontimer = 7,
		weaponvelocity = 550,
		startvelocity = 450,
		weaponacceleration = 131,
		turnrate = 24384,
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "Rocklit3",
		soundhit = "xplosml2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 8000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 68,
			arm_aircraft = 155,
			core_aircraft = 155,
		},
	},
	corship_missile = {
		-- used by units
		-- CORE_T2_SEA_MissileFrigate
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 102,
		name = "Missiles",
		rendertype = 1,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 700,  -- TA 3.1c (was 850)  -- 700
		reloadtime = 2,
		weapontimer = 5,
		weaponvelocity = 450,
		startvelocity = 400,
		weaponacceleration = 121,
		turnrate = 30000,  -- TA 3.1c (was 15000)  -- 30000
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "rockhvy2",
		soundhit = "xplomed2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 8000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 62,  -- 62
			arm_aircraft = 111,
			core_aircraft = 111,
		},
	},
	["core_anti-air_ship_missile"] = {
		-- used by units
		-- CORE_T2_SEA_MissileFrigate
		-- type
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 178,
		name = "Missiles",
		rendertype = 1,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 710,
		reloadtime = 2,
		weapontimer = 5,
		weaponvelocity = 450,
		startvelocity = 430,
		weaponacceleration = 121,
		turnrate = 30000,
		areaofeffect = 48,
		metalpershot = 0,
		soundstart = "rockhvy2",
		soundhit = "xplomed2",
		firestarter = 70,
		smokedelay = .1,
		guidance = 1,
		tracks = 1,
		selfprop = 1,
		smoketrail = 1,
		tolerance = 8000,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 57,
			arm_aircraft = 108,
			core_aircraft = 108,
		},
	},
}
