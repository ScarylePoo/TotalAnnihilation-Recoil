-- Weapon definitions (native Recoil tags; converted from ARM_T2_VEH.TDF)

return {
	arm_bull = {
		name = "Plasma Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 530,  -- 320//560//530
		reloadtime = 1.1,
		weaponvelocity = 330,  -- 210
		areaofeffect = 48,
		craterareaofeffect = 72,
		soundstart = "cannon3",
		soundhit = "xplomed2",
		explosiongenerator = "custom:LITTLEBANG_Expl",
		damage = {
			default = 127,  -- 110 7-10-97//147
		},
	},
	arm_artillery = {
		name = "Plasma Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 1100,  -- 620//1250
		reloadtime = 2.5,
		weaponvelocity = 420,  -- 310//415
		areaofeffect = 85,  -- 48
		craterareaofeffect = 127.5,
		soundstart = "cannhvy2",
		soundhit = "xplomed4",
		accuracy = 500,  -- 2000
		explosiongenerator = "custom:PLASMA_Expl",
		cratermult = .5,
		craterboost = .5,
		impulsefactor = .7,
		damage = {
			default = 170,
		},
	},
	armlatnk_weapon = {
		name = "Lightning Gun",
		weapontype = "LightningCannon",
		rgbcolor = "0.000 1.000 0.800",
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 240,  -- 210
		reloadtime = 1.55,
		weaponvelocity = 400,
		areaofeffect = 8,
		craterareaofeffect = 12,
		duration = 10,
		soundtrigger = 1,
		soundstart = "lghthvy1",
		soundhit = "lashit",
		firestarter = 50,
		damage = {
			default = 200,  -- 120
		},
	},
	arm_paralyzer = {
		name = "Paralyzer",
		weapontype = "LaserCannon",
		rgbcolor = "1.000 0.000 0.482",
		turret = 1,
		paralyzer = 1,
		avoidfriendly = 0,
		collidefriendly = 0,
		range = 550,  -- 220 //380
		reloadtime = 1.2,
		weaponvelocity = 800,
		areaofeffect = 8,
		craterareaofeffect = 12,
		duration = .04,
		soundtrigger = 1,
		soundstart = "lasrlit1",
		soundhit = "lashit",
		-- Redish
		damage = {
			default = 1200,
			-- 15 seconds of paralysis
		},
	},
	arm_mediumcannon = {
		name = "Plasma Cannon",
		weapontype = "Cannon",
		rgbcolor = "1.0 0.5 0.0",
		gravityaffected = true,
		avoidfriendly = 0,
		collidefriendly = 0,
		turret = 1,
		range = 340,  -- 320//560
		reloadtime = 1.8,
		weaponvelocity = 270,  -- 210
		areaofeffect = 48,
		craterareaofeffect = 72,
		soundstart = "cannon2",
		soundhit = "xplomed4",
		explosiongenerator = "custom:LITTLEPLASMA_Expl",
		damage = {
			default = 160,  -- 112//140
		},
	},
}
