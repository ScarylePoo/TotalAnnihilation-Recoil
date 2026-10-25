-- Weapon definitions (native Recoil tags; converted from CORE_T2_AIR.TDF)

return {
	vtol_rocket = {
		name = "Rockets",
		weapontype = "MissileLauncher",
		rgbcolor = "1.000 0.000 0.000",
		avoidfriendly = 0,
		collidefriendly = 0,
		model = "missile",
		range = 520,  -- 450
		reloadtime = 2,
		weapontimer = 5,
		weaponvelocity = 350,
		startvelocity = 100,
		weaponacceleration = 51,
		metalpershot = 0,
		turnrate = 5680,  -- 7680
		areaofeffect = 48,
		craterareaofeffect = 72,
		soundstart = "rocklit3",
		soundhit = "explode",
		firestarter = 70,
		smoketrail = 1,
		tolerance = 8000,
		damage = {
			default = 145,  -- 125
		},
	},
	vtol_rocket2 = {
		name = "Rockets",
		weapontype = "MissileLauncher",
		rgbcolor = "1.000 0.000 0.000",
		avoidfriendly = 0,
		collidefriendly = 0,
		model = "missile",
		range = 520,  -- 450
		reloadtime = 2,
		weapontimer = 5,
		weaponvelocity = 350,
		startvelocity = 250,
		weaponacceleration = 131,
		metalpershot = 0,
		turnrate = 4680,  -- 7680
		areaofeffect = 48,
		craterareaofeffect = 72,
		soundstart = "rocklit3",
		soundhit = "explode",
		firestarter = 70,
		smoketrail = 1,
		tolerance = 8000,
		damage = {
			default = 145,  -- 125
		},
	},
}
