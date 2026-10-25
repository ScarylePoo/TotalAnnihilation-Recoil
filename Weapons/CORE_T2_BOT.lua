-- Weapon definitions (native Recoil tags; converted from CORE_T2_BOT.TDF)

return {
	coramph_weapon1 = {
		name = "Plasma Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 402,  -- 230
		reloadtime = 1.9,
		weaponvelocity = 210,
		areaofeffect = 48,
		craterareaofeffect = 72,
		soundstart = "cannon1",
		soundhit = "xplomed3",
		damage = {
			default = 80,  -- 105
		},
	},
	core_mort = {
		name = "Plasma Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1000,  -- 655//1146
		reloadtime = 2.45,  -- 1.45
		weaponvelocity = 400,  -- 290
		areaofeffect = 36,
		craterareaofeffect = 54,
		soundstart = "cannon1",
		soundhit = "xplomed3",
		damage = {
			default = 105,  -- 55
		},
	},
	flamethrower = {
		name = "Flame Thrower",
		weapontype = "Flame",
		rgbcolor = "1.000 0.000 0.000",
		-- ballistic=1;
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 260,  -- 160//240//220
		reloadtime = 1.2,  -- 1.2//.68
		weapontimer = 1,
		weaponvelocity = 150,  -- 188//110//130
		areaofeffect = 42,  -- 32
		craterareaofeffect = 63,
		burst = 17,  -- 17
		burstrate = .04,  -- .4
		sprayangle = 1024,  -- 1024
		soundstart = "Flamhvy1",
		soundhit = "burn02",
		firestarter = 100,
		groundbounce = 1,
		tolerance = 200,
		damage = {
			default = 16,  -- 10//20
			-- firethrower=2;
		},
	},
}
