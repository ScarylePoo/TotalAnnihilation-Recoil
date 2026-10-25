-- Weapon definitions (converted from ARM_T1_DEF.TDF)

return {
	armfixed_gun = {
		id = 70,
		name = "Plasma Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1550,
		reloadtime = 3,
		weaponvelocity = 470,
		areaofeffect = 64,
		soundstart = "cannhvy5",
		soundhit = "xplomed2",
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
			default = 360,
		},
	},
}
