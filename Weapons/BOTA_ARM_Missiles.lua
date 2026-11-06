-- Weapon definitions (converted from BOTA_ARM_Missiles.TDF)

return {
	armvtol_missile = {
		-- used by units
		-- ARM_T1_AIR_FreedomFighter
		-- type
		weapontype = "MissileLauncher",
		tolerance = 8000,
		tracks = 1,
		-- visuals
		model = "missile",
		smoketrail = 1,
		-- sounds
		soundstart = "Rocklit3",
		soundhit = "xplosml2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 70,
		weapontimer = 5,
		weaponvelocity = 480,
		startvelocity = 420,
		weaponacceleration = 146,
		turnrate = 16384,
		-- stats
		range = 510,  -- TA 3.1c (was 630)
		reloadtime = 3,  -- TA 3.1c (was 5)
		areaofeffect = 48,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 44,  -- TA 3.1c (was 130)
			arm_aircraft = 130,
			core_aircraft = 130,
		},
	},
	armkbot_missile = {
		-- used by units
		-- ARM_T1_BOT_Jethro
		-- ARM_T1_SEA_Skeeter
		-- ARM_T2_VEH_Panther
		-- type
		weapontype = "MissileLauncher",
		turret = 1,
		tolerance = 9000,
		tracks = 1,
		-- visuals
		model = "missile",
		smoketrail = 1,
		-- sounds
		soundstart = "rocklit1",
		soundhit = "xplosml2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 70,
		weapontimer = 5,
		weaponvelocity = 650,
		startvelocity = 450,
		weaponacceleration = 101,
		turnrate = 33000,  -- TA 3.1c (was 17000)  -- 33000
		-- stats
		range = 604,  -- TA 3.1c (was 804)
		reloadtime = 2.4,
		areaofeffect = 48,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 31,  -- TA 3.1c (was 42)
			arm_aircraft = 83,
			core_aircraft = 83,
		},
	},
	armrl_missile = {
		-- used by units
		-- ARM_T1_DEF_Defender
		-- ARM_T1_SEADEF_Defender
		-- type
		weapontype = "MissileLauncher",
		turret = 1,
		tolerance = 10000,
		tracks = 1,
		-- visuals
		model = "missile",
		smoketrail = 1,
		-- sounds
		soundstart = "rockhvy2",
		soundhit = "xplomed2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 70,
		weapontimer = 5,
		weaponvelocity = 660,
		startvelocity = 470,
		weaponacceleration = 154,
		turnrate = 50000,  -- TA 3.1c (was 20000)
		-- stats
		range = 700,  -- TA 3.1c (was 820)
		reloadtime = 2,
		areaofeffect = 48,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 46,  -- TA 3.1c (was 68)
			arm_aircraft = 97,
			core_aircraft = 97,
		},
	},
	armah_weapon = {
		-- used by units
		-- ARM_T1_HOV_Swatter
		-- type
		weapontype = "MissileLauncher",
		turret = 1,
		tolerance = 10000,
		tracks = 1,
		-- visuals
		model = "missile",
		smoketrail = 1,
		-- sounds
		soundstart = "rockhvy2",
		soundhit = "xplomed2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 70,
		weapontimer = 5,
		weaponvelocity = 690,
		startvelocity = 420,
		weaponacceleration = 164,
		turnrate = 50000,
		-- stats
		range = 650,  -- TA 3.1c (was 820)
		reloadtime = 2.1,
		areaofeffect = 48,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 49,
			arm_aircraft = 105,
			core_aircraft = 105,
		},
	},
	armseap_weapon3 = {
		-- used by units
		-- ARM_T1_SEAPL_Albatross
		-- type
		weapontype = "MissileLauncher",
		tolerance = 8000,
		tracks = 1,
		-- visuals
		model = "missile",
		smoketrail = 1,
		-- sounds
		soundstart = "Rocklit3",
		soundhit = "xplosml2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 70,
		weapontimer = 5,
		weaponvelocity = 480,
		startvelocity = 420,
		weaponacceleration = 146,
		turnrate = 16384,
		-- stats
		range = 510,  -- TA 3.1c (was 610)
		reloadtime = 3,
		areaofeffect = 48,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 44,
			arm_aircraft = 130,
			core_aircraft = 130,
		},
	},
	arm_seaplane_fighter_missile = {
		-- used by units
		-- ARM_T1_SEAPL_Tornado
		-- type
		weapontype = "MissileLauncher",
		tolerance = 8000,
		tracks = 1,
		-- visuals
		model = "missile",
		smoketrail = 1,
		-- sounds
		soundstart = "Rocklit3",
		soundhit = "xplosml2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 70,
		weapontimer = 6,
		weaponvelocity = 522,
		startvelocity = 420,
		weaponacceleration = 146,
		turnrate = 19384,
		-- stats
		range = 510,
		reloadtime = 3,
		areaofeffect = 48,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 50,
			arm_aircraft = 140,
			core_aircraft = 140,
		},
	},
	armtruck_missile = {
		-- used by units
		-- ARM_T1_VEH_Samson
		-- type
		weapontype = "MissileLauncher",
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 104,
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
		weaponvelocity = 540,
		startvelocity = 450,
		weaponacceleration = 141,
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
			default = 40,  -- TA 3.1c (was 54)  -- 40//62
			arm_aircraft = 90,
			core_aircraft = 90,
		},
	},
	armvtol_advmissile2 = {
		-- TA 3.1c weapon armvtol_advmissile2 (BOTA used arm_stealth_fighter_missile for it as well)
		-- used by units
		-- ARM_T2_AIR_Hawk
		-- type
		weapontype = "MissileLauncher",
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 112,
		name = "Guided Missiles",
		rendertype = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		lineofsight = 1,
		model = "missile",
		range = 659,
		reloadtime = 3,
		weapontimer = 7,
		weaponvelocity = 554,  -- TA 3.1c (was 559)
		startvelocity = 450,
		weaponacceleration = 130,
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
			default = 70,
			arm_aircraft = 150,
			core_aircraft = 150,
		},
	},
	armvtol_advmissile = {
		-- TA 3.1c weapon armvtol_advmissile (BOTA used arm_stealth_fighter_missile for it as well)
		-- used by units
		-- ARM_T2_AIR_Hawk
		-- type
		weapontype = "MissileLauncher",
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 112,
		name = "Guided Missiles",
		rendertype = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		lineofsight = 1,
		model = "missile",
		range = 659,
		reloadtime = 3,
		weapontimer = 7,
		weaponvelocity = 559,
		startvelocity = 450,
		weaponacceleration = 130,
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
			default = 70,
			arm_aircraft = 150,
			core_aircraft = 150,
		},
	},
	armamph_weapon2 = {
		-- used by units
		-- ARM_T2_BOT_Pelican
		-- type
		weapontype = "MissileLauncher",
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 38,
		name = "Missiles",
		rendertype = 1,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 700,  -- TA 3.1c (was 800)  -- 700
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
	["arm_anti-air_ship_missile"] = {
		-- used by units
		-- ARM_T2_BOT_Pelican
		-- type
		weapontype = "MissileLauncher",
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 77,
		name = "Missiles",
		rendertype = 1,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 710,  -- TA 3.1c (was 810)  -- 710
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
	armship_missile = {
		-- used by units
		-- ARM_T2_SEA_Ranger
		-- type
		weapontype = "MissileLauncher",
		-- visuals
		-- sounds
		-- behaviour
		-- costs
		-- stats
		id = 103,
		name = "Missiles",
		rendertype = 1,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 710,  -- TA 3.1c (was 860)  -- 710
		reloadtime = 2,
		weapontimer = 5,
		weaponvelocity = 450,
		startvelocity = 430,
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
			default = 57,  -- 57
			arm_aircraft = 108,
			core_aircraft = 108,
		},
	},
}
