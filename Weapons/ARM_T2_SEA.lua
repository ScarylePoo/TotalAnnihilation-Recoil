-- Weapon definitions (converted from ARM_T2_SEA.TDF)

return {
	arm_crus = {
		id = 66,
		name = "Cruiser Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		minbarrelangle = -25,
		range = 1650,  -- 1300
		reloadtime = 2.9,
		weaponvelocity = 590,  -- 350
		areaofeffect = 84,
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
			default = 308,
			-- subs=0;
		},
	},
	arm_bats = {
		id = 68,
		name = "BattleShip Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		minbarrelangle = -25,
		range = 1500,  -- 1250
		reloadtime = 1.4,  -- 2.2
		weaponvelocity = 465,  -- 350
		areaofeffect = 84,
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
			default = 380,
			-- subs=0;
		},
	},
}
