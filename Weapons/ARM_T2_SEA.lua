-- Weapon definitions (native Recoil tags; converted from ARM_T2_SEA.TDF)

return {
	arm_crus = {
		name = "Cruiser Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1650,  -- 1300
		reloadtime = 2.9,
		weaponvelocity = 590,  -- 350
		areaofeffect = 84,
		craterareaofeffect = 126,
		soundstart = "cannhvy1",
		soundhit = "xplomed2",
		accuracy = 300,
		targetmoveerror = .05,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 308,
			-- subs=0;
		},
	},
	arm_bats = {
		name = "BattleShip Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1500,  -- 1250
		reloadtime = 1.4,  -- 2.2
		weaponvelocity = 465,  -- 350
		areaofeffect = 84,
		craterareaofeffect = 126,
		soundstart = "cannhvy1",
		soundhit = "xplomed2",
		accuracy = 300,
		targetmoveerror = .05,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 380,
			-- subs=0;
		},
	},
}
