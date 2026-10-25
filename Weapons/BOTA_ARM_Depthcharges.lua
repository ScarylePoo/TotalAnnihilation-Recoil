-- Weapon definitions (native Recoil tags; converted from BOTA_ARM_Depthcharges.TDF)

return {
	arm_depthcharge = {
		-- used by units
		-- ARM_T1_SEA_Crusader
		-- ARM_T2_SEA_Conqueror
		-- type
		weapontype = "TorpedoLauncher",
		rgbcolor = "1.000 0.000 0.000",
		turret = 0,
		tolerance = 32767,
		tracks = 1,
		waterweapon = 1,
		-- visuals
		model = "BOTA_DepthCharge",
		explosiongenerator = "custom:LITTLESPLUNK",
		-- sounds
		soundstart = "torpedo1",
		soundhit = "xplodep2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		weapontimer = 3,
		weaponvelocity = 110,
		startvelocity = 100,
		weaponacceleration = 15,
		turnrate = 10000,
		-- stats
		range = 410,
		reloadtime = 2.8,
		areaofeffect = 16,
		craterareaofeffect = 24,
		damage = {
			default = 70,
			-- subs=120;
		},
	},
}
