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
		range = 340,  -- 320
		reloadtime = 0.9,  -- 1.9
		weaponvelocity = 270,  -- 210
		areaofeffect = 48,
		soundstart = "cannon2",
		soundhit = "xplomed4",
		explosiongenerator = "custom:MEDTANKSHOT_Expl",
		startsmoke = 1,
		damage = {
			default = 88,  -- 117//147
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
		range = 650,  -- 400//650
		reloadtime = 1.4,
		weaponvelocity = 350,  -- 250
		areaofeffect = 84,
		soundstart = "cannhvy2",
		soundhit = "xplomed4",
		startsmoke = 1,
		explosiongenerator = "custom:PLASMA_Expl",
		damage = {
			default = 206,
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
		range = 1100,  -- 620//1250
		reloadtime = 3,
		weaponvelocity = 370,  -- 310//415
		areaofeffect = 70,  -- 48
		soundstart = "cannhvy2",
		soundhit = "xplomed4",
		accuracy = 500,  -- 2000
		explosiongenerator = "custom:PLASMA_Expl",
		startsmoke = 1,
		damage = {
			default = 180,
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
		range = 560,  -- 320//560//530//500
		reloadtime = 1.3,
		weaponvelocity = 330,  -- 210
		areaofeffect = 48,
		soundstart = "cannon3",
		soundhit = "xplomed2",
		explosiongenerator = "custom:LITTLEBANG_Expl",
		startsmoke = 1,
		damage = {
			default = 110,  -- 130 7-10-97//143
		},
	},
}
