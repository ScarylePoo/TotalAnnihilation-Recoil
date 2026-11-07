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
		range = 1300,  -- TA 3.1c (was 1610)  -- 1300 //in range of fixed guns
		reloadtime = 3,
		weaponvelocity = 350,  -- TA 3.1c (was 490)  -- 350
		areaofeffect = 64,  -- TA 3.1c (was 78)
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
		damage = {
			default = 220,  -- TA 3.1c (was 290)
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
		range = 1250,  -- TA 3.1c (was 1300)  -- 1700
		reloadtime = 2.46,  -- TA 3.1c (was 2.0)  -- 2.46
		weaponvelocity = 350,  -- TA 3.1c (was 465)  -- 350
		areaofeffect = 64,  -- TA 3.1c (was 94)
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
		damage = {
			default = 270,  -- TA 3.1c (was 390)
		},
	},
}
