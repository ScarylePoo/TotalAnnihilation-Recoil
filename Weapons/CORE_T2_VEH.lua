-- Weapon definitions (converted from CORE_T2_VEH.TDF)

return {
	core_mediumcannon = {
		id = 53,
		name = "Plasma Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 320,  -- TA 3.1c (was 340)  -- 320
		reloadtime = 1.9,  -- TA 3.1c (was 0.9)  -- 1.9
		weaponvelocity = 220,  -- TA 3.1c (was 270)  -- 210
		areaofeffect = 48,
		soundstart = "cannon2",
		soundhit = "xplomed4",
		explosiongenerator = "custom:MEDTANKSHOT_Expl",
		startsmoke = 1,
		damage = {
			default = 127,  -- TA 3.1c (was 88)  -- 117//147
		},
	},
	cor_gol = {
		id = 62,
		name = "Heavy Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 400,  -- TA 3.1c (was 650)  -- 400//650
		reloadtime = 1.5,  -- TA 3.1c (was 1.4)
		weaponvelocity = 250,  -- TA 3.1c (was 350)  -- 250
		areaofeffect = 64,  -- TA 3.1c (was 84)
		soundstart = "cannhvy2",
		soundhit = "xplomed4",
		startsmoke = 1,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 196,  -- TA 3.1c (was 206)
		},
	},
	core_artillery = {
		id = 59,
		name = "Plasma Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 620,  -- TA 3.1c (was 1100)  -- 620//1250
		reloadtime = 2.95,  -- TA 3.1c (was 3)
		weaponvelocity = 310,  -- TA 3.1c (was 370)  -- 310//415
		areaofeffect = 48,  -- TA 3.1c (was 70)  -- 48
		soundstart = "cannhvy2",
		soundhit = "xplomed4",
		accuracy = 2000,  -- TA 3.1c (was 500)  -- 2000
		explosiongenerator = "custom:PLASMA_Expl",
		startsmoke = 1,
		damage = {
			default = 140,  -- TA 3.1c (was 180)
		},
	},
	core_reap = {
		id = 57,
		name = "Plasma Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 320,  -- TA 3.1c (was 560)  -- 320//560//530//500
		reloadtime = 1.3,
		weaponvelocity = 210,  -- TA 3.1c (was 330)  -- 210
		areaofeffect = 48,
		soundstart = "cannon3",
		soundhit = "xplomed2",
		explosiongenerator = "custom:LITTLEBANG_Expl",
		startsmoke = 1,
		damage = {
			default = 143,  -- TA 3.1c (was 110)  -- 130 7-10-97//143
		},
	},
}
