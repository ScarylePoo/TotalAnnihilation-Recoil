-- Weapon definitions (native Recoil tags; converted from ARM_T1_VEH.TDF)

return {
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
		range = 255,
		reloadtime = 0.4,
		weapontimer = 1,
		weaponvelocity = 400,
		sprayangle = 768,
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
			default = 14,
		},
	},
	arm_lightcannon = {
		name = "Light Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 420,  -- 240
		reloadtime = 1.33,
		weaponvelocity = 350,  -- 170
		areaofeffect = 32,
		craterareaofeffect = 48,
		soundstart = "canlite3",
		soundhit = "xplosml3",
		explosiongenerator = "custom:TANKSHOT_Expl",
		damage = {
			default = 70,  -- 50//75
		},
	},
}
