-- Weapon definitions (converted from CORE_T1_VEH.TDF)

return {
	corlevlr_weapon = {
		id = 172,
		name = "Light Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 500,  -- 260//455
		reloadtime = 1.73,
		weaponvelocity = 280,
		areaofeffect = 84,
		soundstart = "canlite3",
		soundhit = "xplosml3",
		tolerance = 2000,
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 280,  -- 180
		},
	},
	core_lightcannon = {
		id = 51,
		name = "Light Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 420,  -- 240
		reloadtime = 1.43,
		weaponvelocity = 350,  -- 170
		areaofeffect = 32,
		soundstart = "canlite3",
		soundhit = "xplosml3",
		explosiongenerator = "custom:TANKSHOT_Expl",
		startsmoke = 1,
		damage = {
			default = 70,  -- 50//75
		},
	},
}
