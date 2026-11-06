-- Weapon definitions (converted from ARM_T2_VEH.TDF)

return {
	arm_bull = {
		id = 56,
		name = "Plasma Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 320,  -- TA 3.1c (was 530)  -- 320//560//530
		reloadtime = 1.4,  -- TA 3.1c (was 1.1)
		weaponvelocity = 210,  -- TA 3.1c (was 330)  -- 210
		areaofeffect = 48,
		soundstart = "cannon3",
		soundhit = "xplomed2",
		explosiongenerator = "custom:LITTLEBANG_Expl",
		startsmoke = 1,
		damage = {
			default = 147,  -- TA 3.1c (was 127)  -- 110 7-10-97//147
		},
	},
	arm_artillery = {
		id = 58,
		name = "Plasma Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 620,  -- TA 3.1c (was 1100)  -- 620//1250
		reloadtime = 2.75,  -- TA 3.1c (was 2.5)
		weaponvelocity = 310,  -- TA 3.1c (was 420)  -- 310//415
		areaofeffect = 48,  -- TA 3.1c (was 85)  -- 48
		soundstart = "cannhvy2",
		soundhit = "xplomed4",
		accuracy = 2000,  -- TA 3.1c (was 500)  -- 2000
		explosiongenerator = "custom:PLASMA_Expl",
		cratermult = .5,
		craterboost = .5,
		impulsefactor = .7,
		startsmoke = 1,
		damage = {
			default = 130,  -- TA 3.1c (was 170)
		},
	},
	armlatnk_weapon = {
		id = 166,
		name = "Lightning Gun",
		rendertype = 7,
		lineofsight = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 210,  -- TA 3.1c (was 240)  -- 210
		reloadtime = 1.55,
		weaponvelocity = 400,
		areaofeffect = 8,
		duration = 10,
		soundtrigger = 1,
		soundstart = "lghthvy1",
		soundhit = "lashit",
		firestarter = 50,
		beamweapon = 1,
		color = 119,  -- 208	/* Yellow */
		color2 = 240,  -- 196
		explosiongaf = "fx",
		explosionart = "explode5",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom1",
		startsmoke = 1,
		damage = {
			default = 120,  -- TA 3.1c (was 200)  -- 120
		},
	},
	arm_paralyzer = {
		id = 29,
		name = "Paralyzer",
		rendertype = 0,
		lineofsight = 1,
		turret = 1,
		paralyzer = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		minbarrelangle = 0,
		range = 220,  -- TA 3.1c (was 550)  -- 220 //380
		reloadtime = 1.2,
		weaponvelocity = 600,  -- TA 3.1c (was 800)
		areaofeffect = 8,
		duration = .04,
		soundtrigger = 1,
		soundstart = "lasrlit1",
		soundhit = "lashit",
		beamweapon = 1,
		color = 209,
		-- Redish
		color2 = 211,
		explosiongaf = "fx",
		explosionart = "explode5",
		waterexplosiongaf = "fx",
		waterexplosionart = "h2oboom1",
		damage = {
			default = 900,  -- TA 3.1c (was 1200)
		},
	},
	arm_mediumcannon = {
		id = 52,
		name = "Plasma Cannon",
		rendertype = 4,
		ballistic = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 320,  -- TA 3.1c (was 340)  -- 320//560
		reloadtime = 1.8,
		weaponvelocity = 210,  -- TA 3.1c (was 270)  -- 210
		areaofeffect = 48,
		soundstart = "cannon2",
		soundhit = "xplomed4",
		explosiongenerator = "custom:LITTLEPLASMA_Expl",
		startsmoke = 1,
		damage = {
			default = 112,  -- TA 3.1c (was 160)  -- 112//140
		},
	},
}
