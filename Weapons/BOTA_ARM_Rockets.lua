-- Weapon definitions (native Recoil tags; converted from BOTA_ARM_Rockets.TDF)

return {
	arm_hover_rocket = {
		-- used by units
		-- ARM_T1_HOV_Wombat
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
		tolerance = 4000,
		-- visuals
		model = "BOTA_ARM_Hover_Rocket",
		smoketrail = 1,
		-- sounds
		soundstart = "Rockhvy1",
		soundhit = "xplomed4",
		-- behaviour
		avoidfriendly = 1,
		collidefriendly = 1,
		firestarter = 100,
		weapontimer = 5,
		flighttime = 10,
		weaponvelocity = 400,
		weaponacceleration = 40,
		turnrate = 24384,
		-- stats
		range = 1100,
		reloadtime = 12,
		areaofeffect = 140,
		craterareaofeffect = 210,
		edgeeffectiveness = 0.75,
		damage = {
			default = 600,
		},
	},
	arm_ship_rocket = {
		-- used by units
		-- ARM_T2_SEA_Ranger
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
		tolerance = 4000,
		-- visuals
		model = "BOTA_Rocket",
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
		range = 1630,
		reloadtime = 12,
		areaofeffect = 215,
		craterareaofeffect = 322.5,
		edgeeffectiveness = 0.50,
		damage = {
			default = 900,
		},
	},
	arm_veh_rocket = {
		-- used by units
		-- ARM_T2_VEH_Merl
		-- type
		weapontype = "StarburstLauncher",
		rgbcolor = "1.000 0.000 0.000",
		tolerance = 4000,
		-- visuals
		model = "BOTA_Rocket",
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
		range = 1200,
		reloadtime = 12,
		edgeeffectiveness = 0.75,
		areaofeffect = 150,
		craterareaofeffect = 225,
		damage = {
			default = 600,
		},
	},
}
