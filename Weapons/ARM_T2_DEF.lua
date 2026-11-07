-- Weapon definitions (converted from ARM_T2_DEF.TDF)

return {
	armamb_gun = {
		id = 40,
		name = "Pop-up Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 910,  -- TA 3.1c (was 1300)  -- 910//1250
		reloadtime = 3.1,
		weaponvelocity = 350,  -- TA 3.1c (was 420)  -- 350
		areaofeffect = 100,
		soundstart = "cannhvy5",
		soundhit = "xplomed2",
		minbarrelangle = -35,
		accuracy = 300,
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		damage = {
			default = 310,
		},
	},
}
