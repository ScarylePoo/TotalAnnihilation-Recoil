-- Weapon definitions (converted from ARM_T1_BOT.TDF)

return {
	arm_ham = {
		id = 54,
		name = "Plasma Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		minbarrelangle = -35,
		range = 320,  -- TA 3.1c (was 590)  -- 320//500//690//630//650//530
		reloadtime = 1.95,  -- TA 3.1c (was 2.57)  -- 1.95//2.4//3.4//1.95
		weaponvelocity = 210,  -- TA 3.1c (was 270)  -- 210//270//305
		areaofeffect = 48,
		soundstart = "cannon1",
		soundhit = "xplomed3",
		startsmoke = 1,
		damage = {
			default = 85,  -- TA 3.1c (was 105)
		},
	},
	emg = {
		weapontype = "Cannon",  -- TA E.M.G. as a Cannon instead of EmgCannon (user decision: EmgCannon is poorly maintained in Recoil); it now has gravity
		rgbcolor = "0.9 0.9 0.2",  -- TA E.M.G. yellow
		id = 16,
		name = "E.M.G.",
		-- 2D bitmap
		-- EMG bitmap shell, its a hack
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		-- model=plasma;
		range = 180,  -- TA 3.1c (was 255)  -- 280 180 255//255
		reloadtime = 0.4,
		weapontimer = 1,
		weaponvelocity = 300,  -- TA 3.1c (was 400)  -- 300
		sprayangle = 1024,  -- TA 3.1c (was 768)  -- 1024
		areaofeffect = 8,
		burst = 3,  -- TA 3.1c (was 4)
		burstrate = .1,
		soundstart = "armsml2",
		soundhit = "lasrhit1",
		soundtrigger = 1,
		tolerance = 6000,
		startsmoke = 1,
		damage = {
			default = 8,  -- TA 3.1c (was 14)  -- 10 16
		},
	},
	kbot_rocket = {
		id = 120,
		name = "Rockets",
		rendertype = 1,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		model = "missile",
		range = 400,  -- TA 3.1c (was 500)  -- 400//690
		reloadtime = 4,  -- TA 3.1c (was 8.3)  -- 8//6//6.5
		weapontimer = 2,
		weaponvelocity = 250,
		startvelocity = 250,
		weaponacceleration = 120,
		areaofeffect = 48,
		metalpershot = 0,
		burst = 3,
		burstrate = 1,
		soundstart = "rocklit1",
		soundhit = "xplosml2",
		firestarter = 70,
		smokedelay = .1,
		selfprop = 1,
		smoketrail = 1,
		explosiongaf = "fx",
		explosionart = "explode3",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 105,  -- TA 3.1c (was 110)  -- 250//220
		},
	},
	armwar_emg = {
		weapontype = "Cannon",  -- TA E.M.G. as a Cannon instead of EmgCannon (user decision: EmgCannon is poorly maintained in Recoil); it now has gravity
		rgbcolor = "0.9 0.9 0.2",  -- TA E.M.G. yellow
		id = 171,
		name = "E.M.G.",
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 180,  -- TA 3.1c (was 320)  -- 180
		reloadtime = 0.4,
		weapontimer = 1,
		weaponvelocity = 300,  -- TA 3.1c (was 500)  -- 300
		sprayangle = 1024,  -- TA 3.1c (was 512)  -- 1024
		areaofeffect = 8,
		burst = 2,  -- TA 3.1c (was 4)
		burstrate = 0.2,  -- TA 3.1c (was .07)
		soundstart = "armsml2",
		soundhit = "lasrhit1",
		soundtrigger = 1,
		tolerance = 5000,
		startsmoke = 1,
		explosiongaf = "fx",
		explosionart = "explode5",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom1",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplashsm",
		damage = {
			default = 12,  -- TA 3.1c (was 20)  -- 12//16
		},
	},
	armwar_lcannon = {
		id = 176,
		name = "Light Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 240,  -- TA 3.1c (was 420)  -- 240
		reloadtime = 2.13,
		weaponvelocity = 170,  -- TA 3.1c (was 250)  -- 170
		areaofeffect = 32,
		soundstart = "canlite3",
		soundhit = "xplosml3",
		tolerance = 3000,
		explosiongaf = "fx",
		explosionart = "explode4",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 60,  -- TA 3.1c (was 80)
		},
	},
}
