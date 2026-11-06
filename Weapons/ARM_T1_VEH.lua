-- Weapon definitions (converted from ARM_T1_VEH.TDF)

return {
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
		range = 180,  -- TA 3.1c (was 255)
		reloadtime = 0.4,
		weapontimer = 1,
		weaponvelocity = 300,  -- TA 3.1c (was 400)
		sprayangle = 1024,  -- TA 3.1c (was 768)
		areaofeffect = 8,
		burst = 3,  -- TA 3.1c (was 4)
		burstrate = .1,
		soundstart = "armsml2",
		soundhit = "lasrhit1",
		soundtrigger = 1,
		tolerance = 6000,
		explosiongenerator = "custom:FLASH1white",
		startsmoke = 1,
		damage = {
			default = 8,  -- TA 3.1c (was 14)
		},
	},
	arm_lightcannon = {
		id = 50,
		name = "Light Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 240,  -- TA 3.1c (was 420)  -- 240
		reloadtime = 1.53,  -- TA 3.1c (was 1.33)
		weaponvelocity = 170,  -- TA 3.1c (was 350)  -- 170
		areaofeffect = 32,
		soundstart = "canlite3",
		soundhit = "xplosml3",
		explosiongenerator = "custom:TANKSHOT_Expl",
		startsmoke = 1,
		damage = {
			default = 50,  -- TA 3.1c (was 70)  -- 50//75
		},
	},
}
