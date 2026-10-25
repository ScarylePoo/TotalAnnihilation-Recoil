-- Weapon definitions (converted from CORE_T2_SEA.TDF)

return {
	cor_crus = {
		id = 67,
		name = "Cruiser Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		minbarrelangle = -25,
		range = 1610,  -- 1300 //in range of fixed guns
		reloadtime = 3,
		weaponvelocity = 490,  -- 350
		areaofeffect = 78,
		soundstart = "cannhvy1",
		soundhit = "xplomed2",
		accuracy = 300,
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		targetmoveerror = .05,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 290,
			-- subs=0;
		},
	},
	cor_bats = {
		id = 69,
		name = "BattleShip Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		minbarrelangle = -25,
		range = 1300,  -- 1700
		reloadtime = 2.0,  -- 2.46
		weaponvelocity = 465,  -- 350
		areaofeffect = 94,
		soundstart = "cannhvy1",
		soundhit = "xplomed2",
		accuracy = 300,
		explosiongaf = "fx",
		explosionart = "explode2",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2o",
		lavaexplosiongaf = "fx",
		lavaexplosionart = "lavasplash",
		startsmoke = 1,
		targetmoveerror = .05,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 390,
			-- subs=0;
		},
	},
}
