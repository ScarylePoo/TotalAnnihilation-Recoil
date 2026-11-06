-- Weapon definitions (converted from BOTA_CORE_Rockets.TDF)

return {
	core_hover_rocket = {
		-- used by units
		-- CORE_T1_HOV_Nixer
		-- type
		weapontype = "StarburstLauncher",
		tolerance = 4000,
		-- visuals
		model = "cormhmsl",
		smoketrail = 1,
		-- sounds
		soundstart = "Rockhvy1",
		soundhit = "xplomed4",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 1,
		firestarter = 100,
		weapontimer = 5,
		flighttime = 10,
		weaponvelocity = 400,
		weaponacceleration = 40,
		turnrate = 24384,
		-- stats
		range = 650,  -- TA 3.1c (was 1100)
		reloadtime = 9,  -- TA 3.1c (was 13)
		areaofeffect = 80,  -- TA 3.1c (was 140)
		edgeeffectiveness = 0.75,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 320,  -- TA 3.1c (was 600)
		},
	},
	core_kbot_rocket = {
		-- used by units
		-- CORE_T2_BOT_Dominator
		-- type
		weapontype = "StarburstLauncher",
		tolerance = 1000,
		-- visuals
		model = "CorKBMissl1",
		smoketrail = 1,
		-- sounds
		soundstart = "Rockhvy1",
		soundhit = "xplomed4",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 1,
		firestarter = 100,
		weapontimer = 5,
		flighttime = 10,
		weaponvelocity = 350,
		weaponacceleration = 34,
		turnrate = 28384,
		-- stats
		range = 600,  -- TA 3.1c (was 1000)
		reloadtime = 8,  -- TA 3.1c (was 12)
		areaofeffect = 60,  -- TA 3.1c (was 140)
		edgeeffectiveness = 0.5,  -- TA 3.1c (was 0.75)
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 240,  -- TA 3.1c (was 500)
		},
	},
	core_ship_rocket = {
		-- used by units
		-- CORE_T2_SEA_MissileFrigate
		-- type
		weapontype = "StarburstLauncher",
		tolerance = 4000,
		-- visuals
		model = "corshiprckt1",
		smoketrail = 1,
		-- sounds
		soundstart = "Rockhvy1",
		soundhit = "xplomed4",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 1,
		firestarter = 100,
		weapontimer = 5,
		flighttime = 10,
		weaponvelocity = 400,
		weaponacceleration = 40,
		turnrate = 24384,
		-- stats
		range = 1300,  -- TA 3.1c (was 1680)
		reloadtime = 9,
		areaofeffect = 96,  -- TA 3.1c (was 215)
		edgeeffectiveness = 0.50,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 500,  -- TA 3.1c (was 900)
		},
	},
	core_veh_rocket = {
		-- used by units
		-- CORE_T2_VEH_Diplomat
		-- type
		weapontype = "StarburstLauncher",
		tolerance = 4000,
		-- visuals
		model = "corvrocket",
		smoketrail = 1,
		-- sounds
		soundstart = "Rockhvy1",
		soundhit = "xplomed4",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 1,
		firestarter = 100,
		weapontimer = 5,
		flighttime = 10,
		weaponvelocity = 375,
		weaponacceleration = 38,
		turnrate = 24384,
		-- stats
		range = 800,  -- TA 3.1c (was 1200)
		reloadtime = 13,
		areaofeffect = 96,  -- TA 3.1c (was 150)
		edgeeffectiveness = 0.75,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 500,  -- TA 3.1c (was 600)
		},
	},
	krogoth_rocket = {
		-- used by units
		-- CORE_T3_BOT_Krogoth
		-- type
		weapontype = "StarburstLauncher",
		tolerance = 9000,
		tracks = 1,
		-- visuals
		model = "BOTA_Anti_Nuclear_Missile",
		smoketrail = 1,
		-- sounds
		soundstart = "rocklit1",
		soundhit = "xplosml2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 1,
		firestarter = 70,
		weapontimer = 5,  -- TA 3.1c (was 2)
		flighttime = 15,  -- TA 3.1c (was 7)
		startvelocity = 250,
		weaponacceleration = 200,
		weaponvelocity = 550,
		turnrate = 63000,
		-- stats
		range = 900,  -- TA 3.1c (was 1300)
		reloadtime = 1.4,
		areaofeffect = 80,  -- TA 3.1c (was 120)
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 131,  -- TA 3.1c (was 251)
			arm_aircraft = 383,
			core_aircraft = 383,
		},
	},
}
