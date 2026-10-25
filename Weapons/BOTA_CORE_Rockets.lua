-- Weapon definitions (native Recoil tags; converted from BOTA_CORE_Rockets.TDF)

return {
	core_hover_rocket = {
		-- used by units
		-- CORE_T1_HOV_Nixer
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		range = 1100,
		reloadtime = 13,
		areaofeffect = 140,
		craterareaofeffect = 210,
		edgeeffectiveness = 0.75,
		damage = {
			default = 600,
		},
	},
	core_kbot_rocket = {
		-- used by units
		-- CORE_T2_BOT_Dominator
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		range = 1000,
		reloadtime = 12,
		areaofeffect = 140,
		craterareaofeffect = 210,
		edgeeffectiveness = 0.75,
		damage = {
			default = 500,
		},
	},
	core_ship_rocket = {
		-- used by units
		-- CORE_T2_SEA_MissileFrigate
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		range = 1680,
		reloadtime = 9,
		areaofeffect = 215,
		craterareaofeffect = 322.5,
		edgeeffectiveness = 0.50,
		damage = {
			default = 900,
		},
	},
	core_veh_rocket = {
		-- used by units
		-- CORE_T2_VEH_Diplomat
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		range = 1200,
		reloadtime = 13,
		areaofeffect = 150,
		craterareaofeffect = 225,
		edgeeffectiveness = 0.75,
		damage = {
			default = 600,
		},
	},
	krogoth_rocket = {
		-- used by units
		-- CORE_T3_BOT_Krogoth
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
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
		weapontimer = 2,
		flighttime = 7,
		startvelocity = 250,
		weaponacceleration = 200,
		weaponvelocity = 550,
		turnrate = 63000,
		-- stats
		range = 1300,
		reloadtime = 1.4,
		areaofeffect = 120,
		craterareaofeffect = 180,
		damage = {
			default = 251,
		},
	},
}
