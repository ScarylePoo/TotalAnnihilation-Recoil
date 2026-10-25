-- Weapon definitions (native Recoil tags; converted from CORE_T2_DEF.TDF)

return {
	cortoast_gun = {
		name = "Pop-up Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1300,  -- 885//1200
		reloadtime = 3.2,
		weaponvelocity = 420,  -- 380
		areaofeffect = 105,
		craterareaofeffect = 157.5,
		soundstart = "cannhvy5",
		soundhit = "xplomed2",
		accuracy = 300,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 295,
		},
	},
}
