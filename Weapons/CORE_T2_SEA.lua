-- Weapon definitions (native Recoil tags; converted from CORE_T2_SEA.TDF)

return {
	cor_crus = {
		name = "Cruiser Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1610,  -- 1300 //in range of fixed guns
		reloadtime = 3,
		weaponvelocity = 490,  -- 350
		areaofeffect = 78,
		craterareaofeffect = 117,
		soundstart = "cannhvy1",
		soundhit = "xplomed2",
		accuracy = 300,
		targetmoveerror = .05,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 290,
			-- subs=0;
		},
	},
	cor_bats = {
		name = "BattleShip Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1300,  -- 1700
		reloadtime = 2.0,  -- 2.46
		weaponvelocity = 465,  -- 350
		areaofeffect = 94,
		craterareaofeffect = 141,
		soundstart = "cannhvy1",
		soundhit = "xplomed2",
		accuracy = 300,
		targetmoveerror = .05,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 390,
			-- subs=0;
		},
	},
}
