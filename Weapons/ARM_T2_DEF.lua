-- Weapon definitions (native Recoil tags; converted from ARM_T2_DEF.TDF)

return {
	armamb_gun = {
		name = "Pop-up Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1300,  -- 910//1250
		reloadtime = 3.1,
		weaponvelocity = 420,  -- 350
		areaofeffect = 100,
		craterareaofeffect = 150,
		soundstart = "cannhvy5",
		soundhit = "xplomed2",
		accuracy = 300,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 310,
		},
	},
}
