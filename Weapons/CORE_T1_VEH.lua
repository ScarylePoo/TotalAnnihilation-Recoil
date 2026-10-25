-- Weapon definitions (native Recoil tags; converted from CORE_T1_VEH.TDF)

return {
	corlevlr_weapon = {
		name = "Light Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 500,  -- 260//455
		reloadtime = 1.73,
		weaponvelocity = 280,
		areaofeffect = 84,
		craterareaofeffect = 126,
		soundstart = "canlite3",
		soundhit = "xplosml3",
		tolerance = 2000,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 280,  -- 180
		},
	},
	core_lightcannon = {
		name = "Light Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 420,  -- 240
		reloadtime = 1.43,
		weaponvelocity = 350,  -- 170
		areaofeffect = 32,
		craterareaofeffect = 48,
		soundstart = "canlite3",
		soundhit = "xplosml3",
		explosiongenerator = "custom:TANKSHOT_Expl",
		damage = {
			default = 70,  -- 50//75
		},
	},
}
