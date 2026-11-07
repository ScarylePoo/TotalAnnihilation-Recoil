-- Weapon definitions (converted from ARM_T2_AIR.TDF)

return {
	vtol_emg = {
		weapontype = "Cannon",  -- TA E.M.G. as a Cannon instead of EmgCannon (user decision: EmgCannon is poorly maintained in Recoil); it now has gravity
		rgbcolor = "0.9 0.9 0.2",  -- TA E.M.G. yellow
		id = 18,
		name = "E.M.G.",
		-- 2D bitmap
		-- EMG bitmap
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 0,
		-- model=plasma;
		range = 370,  -- TA 3.1c (was 450)  -- 370//400
		reloadtime = 0.6,
		weapontimer = 1,
		weaponvelocity = 450,
		-- startvelocity=150;
		-- weaponacceleration=200;
		sprayangle = 1024,
		areaofeffect = 8,
		burst = 4,
		burstrate = .1,
		soundstart = "armsml3",
		soundhit = "lasrhit1",
		soundtrigger = 1,
		tolerance = 6000,
		pitchtolerance = 12000,
		startsmoke = 1,
		damage = {
			default = 11,
		},
	},
}
