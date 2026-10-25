-- Weapon definitions (native Recoil tags; converted from ARM_T2_AIR.TDF)

return {
	vtol_emg = {
		name = "E.M.G.",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		-- 2D bitmap
		-- EMG bitmap
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 0,
		-- model=plasma;
		range = 450,  -- 370//400
		reloadtime = 0.6,
		weapontimer = 1,
		weaponvelocity = 450,
		-- startvelocity=150;
		-- weaponacceleration=200;
		sprayangle = 1024,
		areaofeffect = 8,
		craterareaofeffect = 12,
		burst = 4,
		burstrate = .1,
		soundstart = "armsml3",
		soundhit = "lasrhit1",
		soundtrigger = 1,
		tolerance = 6000,
		explosiongenerator = "custom:FLASH1white",
		damage = {
			default = 11,
		},
	},
}
