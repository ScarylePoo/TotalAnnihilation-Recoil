-- Weapon definitions (converted from BOTA_CORE_Depthcharges.TDF)

return {
	core_depthcharge = {
		-- used by units
		-- CORE_T1_SEA_Enforcer
		-- CORE_T2_SEA_Executioner
		-- type
		weapontype = "TorpedoLauncher",
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
		weaponvelocity = 100,
		startvelocity = 100,
		weaponacceleration = 15,
		turnrate = 10000,
		-- stats
		range = 400,
		reloadtime = 2.6,
		areaofeffect = 16,
		damage = {
			default = 80,
			-- subs=130;
		},
	},
}
