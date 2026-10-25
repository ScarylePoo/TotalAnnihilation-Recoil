-- Weapon definitions (native Recoil tags; converted from BOTA_ARM_Lasers.TDF)

return {
	arm_flea_laser = {
		-- used by units
		-- ARM_T1_BOT_Flea
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		tolerance = 500,
		-- visuals
		loddistance = 4000,
		duration = 0.01,
		hardstop = 1,
		thickness = 3,
		rgbcolor = "0.6 0 0",  -- red
		corethickness = 0.3,
		rgbcolor2 = "0.9 0 0",  -- even more red
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrfir3",
		soundhit = "lasrhit2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 30,
		weaponvelocity = 900,
		-- stats
		range = 420,
		reloadtime = 0.8,
		areaofeffect = 8,
		craterareaofeffect = 12,
		damage = {
			default = 8,
		},
	},
	arm_scout_laser = {
		-- used by units
		-- ARM_T1_HOV_Skimmer
		-- ARM_T1_SEA_Skeeter
		-- ARM_T1_VEH_Jeffy
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		tolerance = 500,
		-- visuals
		loddistance = 4000,
		duration = 0.04,
		hardstop = 1,
		thickness = 5,
		rgbcolor = "0.6 0 0",  -- red
		corethickness = 0.3,
		rgbcolor2 = "0.9 0 0",  -- even more red
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrfir1",
		soundhit = "lasrhit2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		weaponvelocity = 900,
		-- stats
		range = 315,
		reloadtime = 1,
		areaofeffect = 8,
		craterareaofeffect = 12,
		damage = {
			default = 23,
		},
	},
	arm_phoenix_laser = {
		-- used by units
		-- ARM_T2_AIR_Phoenix
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		tolerance = 500,
		-- visuals
		loddistance = 4000,
		duration = 0.02,
		hardstop = 1,
		thickness = 3,
		rgbcolor = "0.6 0 0",  -- red
		corethickness = 0.3,
		rgbcolor2 = "0.9 0 0",  -- even more red
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrlit1",
		soundhit = "lashit",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		weaponvelocity = 900,
		-- stats
		range = 600,
		reloadtime = 0.4,
		areaofeffect = 8,
		craterareaofeffect = 12,
		damage = {
			default = 16,
		},
	},
	arm_pelican_laser = {
		-- used by units
		-- ARM_T2_BOT_Pelican
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		tolerance = 500,
		-- visuals
		loddistance = 4000,
		duration = 0.06,
		hardstop = 1,
		thickness = 7,
		rgbcolor = "0.6 0 0",  -- red
		corethickness = 0.3,
		rgbcolor2 = "0.9 0 0",  -- even more red
		-- sounds
		soundstart = "lasrfir3",
		soundhit = "lasrhit2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 20,
		weaponvelocity = 900,
		-- stats
		range = 360,
		reloadtime = 0.9,
		areaofeffect = 8,
		craterareaofeffect = 12,
		damage = {
			default = 70,
		},
	},
	arm_zipper_laser = {
		-- used by units
		-- ARM_T2_BOT_Zipper
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		tolerance = 500,
		-- visuals
		loddistance = 4000,
		duration = 0.05,
		hardstop = 1,
		thickness = 5,
		rgbcolor = "0.6 0 0",  -- red
		corethickness = 0.3,
		rgbcolor2 = "0.9 0 0",  -- even more red
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrfast",
		soundhit = "lashit",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		weaponvelocity = 900,
		-- stats
		range = 367,
		reloadtime = 0.8,
		areaofeffect = 8,
		craterareaofeffect = 12,
		damage = {
			default = 46,
		},
	},
}
