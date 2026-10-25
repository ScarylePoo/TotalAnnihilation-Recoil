-- Weapon definitions (native Recoil tags; converted from CORE_T1_SEA.TDF)

return {
	core_roy = {
		name = "Heavy Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 950,  -- 660//1100
		reloadtime = 2.4,
		weaponvelocity = 380,  -- 300
		areaofeffect = 48,
		craterareaofeffect = 72,
		soundstart = "cannhvy1",
		soundhit = "xplomed2",
		accuracy = 300,
		targetmoveerror = .15,  -- .3
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 180,
			-- subs=0;
		},
	},
}
