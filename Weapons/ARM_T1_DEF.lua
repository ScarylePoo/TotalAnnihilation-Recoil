-- Weapon definitions (native Recoil tags; converted from ARM_T1_DEF.TDF)

return {
	armfixed_gun = {
		name = "Plasma Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1550,
		reloadtime = 3,
		weaponvelocity = 470,
		areaofeffect = 64,
		craterareaofeffect = 96,
		soundstart = "cannhvy5",
		soundhit = "xplomed2",
		accuracy = 300,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 360,
		},
	},
}
