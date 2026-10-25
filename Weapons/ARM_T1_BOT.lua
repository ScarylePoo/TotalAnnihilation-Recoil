-- Weapon definitions (native Recoil tags; converted from ARM_T1_BOT.TDF)

return {
	arm_ham = {
		name = "Plasma Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 590,  -- 320//500//690//630//650//530
		reloadtime = 2.57,  -- 1.95//2.4//3.4//1.95
		weaponvelocity = 270,  -- 210//270//305
		areaofeffect = 48,
		craterareaofeffect = 72,
		soundstart = "cannon1",
		soundhit = "xplomed3",
		explosiongenerator = "custom:MARY_SUE",
		damage = {
			default = 105,
		},
	},
	emg = {
		name = "E.M.G.",
		weapontype = "EmgCannon",
		rgbcolor = "0.9 0.9 0.2",
		-- 2D bitmap
		-- EMG bitmap shell, its a hack
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		-- model=plasma;
		range = 255,  -- 280 180 255//255
		reloadtime = 0.4,
		weapontimer = 1,
		weaponvelocity = 400,  -- 300
		sprayangle = 768,  -- 1024
		areaofeffect = 8,
		craterareaofeffect = 12,
		burst = 4,
		burstrate = .1,
		soundstart = "armsml2",
		soundhit = "lasrhit1",
		soundtrigger = 1,
		tolerance = 6000,
		explosiongenerator = "custom:FLASH1white",
		damage = {
			default = 14,  -- 10 16
		},
	},
	kbot_rocket = {
		name = "Rockets",
		weapontype = "MissileLauncher",
		rgbcolor = "1.000 0.000 0.000",
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 500,  -- 400//690
		reloadtime = 8.3,  -- 8//6//6.5
		weapontimer = 2,
		weaponvelocity = 250,
		startvelocity = 250,
		weaponacceleration = 120,
		areaofeffect = 48,
		craterareaofeffect = 72,
		metalpershot = 0,
		burst = 3,
		burstrate = 1,
		soundstart = "rocklit1",
		soundhit = "xplosml2",
		firestarter = 70,
		smoketrail = 1,
		damage = {
			default = 110,  -- 250//220
		},
	},
	armwar_emg = {
		name = "E.M.G.",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 320,  -- 180
		reloadtime = 0.4,
		weapontimer = 1,
		weaponvelocity = 500,  -- 300
		sprayangle = 512,  -- 1024
		areaofeffect = 8,
		craterareaofeffect = 12,
		burst = 4,
		burstrate = .07,
		soundstart = "armsml2",
		soundhit = "lasrhit1",
		soundtrigger = 1,
		tolerance = 5000,
		damage = {
			default = 20,  -- 12//16
		},
	},
	armwar_lcannon = {
		name = "Light Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 420,  -- 240
		reloadtime = 2.13,
		weaponvelocity = 250,  -- 170
		areaofeffect = 32,
		craterareaofeffect = 48,
		soundstart = "canlite3",
		soundhit = "xplosml3",
		tolerance = 3000,
		damage = {
			default = 80,
		},
	},
}
