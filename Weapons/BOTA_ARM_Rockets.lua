-- Weapon definitions (converted from BOTA_ARM_Rockets.TDF)

return {
	arm_hover_rocket = {
		-- used by units
		-- ARM_T1_HOV_Wombat
		-- type
		weapontype = "StarburstLauncher",
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
		range = 670,  -- TA 3.1c (was 1100)
		reloadtime = 9,  -- TA 3.1c (was 12)
		areaofeffect = 80,  -- TA 3.1c (was 140)
		edgeeffectiveness = 0.75,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 300,  -- TA 3.1c (was 600)
		},
	},
	arm_ship_rocket = {
		-- used by units
		-- ARM_T2_SEA_Ranger
		-- type
		weapontype = "StarburstLauncher",
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
		range = 1300,  -- TA 3.1c (was 1630)
		reloadtime = 12,
		areaofeffect = 96,  -- TA 3.1c (was 215)
		edgeeffectiveness = 0.50,
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 500,  -- TA 3.1c (was 900)
		},
	},
	arm_veh_rocket = {
		-- used by units
		-- ARM_T2_VEH_Merl
		-- type
		weapontype = "StarburstLauncher",
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
		range = 800,  -- TA 3.1c (was 1200)
		reloadtime = 12,
		edgeeffectiveness = 0.75,
		areaofeffect = 96,  -- TA 3.1c (was 150)
		metalpershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 500,  -- TA 3.1c (was 600)
		},
	},
}
