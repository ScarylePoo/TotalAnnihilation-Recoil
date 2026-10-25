-- Weapon definitions (converted from CORE_T2_DEF.TDF)

return {
	cortoast_gun = {
		id = 44,
		name = "Pop-up Cannon",
		rendertype = 4,
		avoidfriendly = 0,
		collidefriendly = 0,
		ballistic = 1,
		turret = 1,
		range = 1300,  -- 885//1200
		reloadtime = 3.2,
		weaponvelocity = 420,  -- 380
		areaofeffect = 105,
		soundstart = "cannhvy5",
		soundhit = "xplomed2",
		minbarrelangle = -40,
		accuracy = 300,
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 295,
		},
	},
}
