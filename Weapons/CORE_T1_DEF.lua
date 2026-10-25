-- Weapon definitions (native Recoil tags; converted from CORE_T1_DEF.TDF)

return {
	corplas_weapon = {
		name = "Immolator",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 560,
		reloadtime = 0.8,
		weaponvelocity = 310,
		areaofeffect = 140,
		craterareaofeffect = 210,
		soundstart = "cannon3",
		soundhit = "xplosml4",
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 40,
		},
	},
	corfixed_gun = {
		name = "Plasma Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1500,
		reloadtime = 2.8,
		weaponvelocity = 460,
		areaofeffect = 85,
		craterareaofeffect = 127.5,
		soundstart = "cannhvy5",
		soundhit = "xplomed2",
		accuracy = 300,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 320,
		},
	},
}
