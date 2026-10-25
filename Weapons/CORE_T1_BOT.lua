-- Weapon definitions (native Recoil tags; converted from CORE_T1_BOT.TDF)

return {
	corkbot_rocket = {
		name = "Rockets",
		weapontype = "MissileLauncher",
		rgbcolor = "1.000 0.000 0.000",
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 500,  -- 400//700//730//690
		reloadtime = 6.6,  -- 3.7//6.1
		weapontimer = 2,
		weaponvelocity = 250,
		startvelocity = 250,
		weaponacceleration = 120,
		areaofeffect = 48,
		craterareaofeffect = 72,
		metalpershot = 0,
		soundstart = "rocklit1",
		soundhit = "xplosml2",
		firestarter = 70,
		smoketrail = 1,
		damage = {
			default = 220,  -- 100//250
		},
	},
	core_thud = {
		name = "Plasma Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 590,  -- 320//403//500//690//630//650//530
		reloadtime = 2.5,  -- 1.9//2.4//3.4//1.9
		weaponvelocity = 270,  -- 210//270//305
		areaofeffect = 48,
		craterareaofeffect = 72,
		soundstart = "cannon1",
		soundhit = "xplomed3",
		explosiongenerator = "custom:MARY_SUE",
		damage = {
			default = 100,  -- 105//80//95
		},
	},
}
