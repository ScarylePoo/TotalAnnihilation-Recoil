-- Weapon definitions (converted from BOTA_ARM_Lasers.TDF)

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
		range = 300,  -- TA 3.1c (was 420)
		reloadtime = 0.8,
		areaofeffect = 8,
		energypershot = 0,  -- TA 3.1c (was unset)
		damage = {
			default = 8,
		},
	},
	armsh_weapon = {
		-- TA 3.1c weapon armsh_weapon (BOTA used arm_scout_laser for it as well)
		-- used by units
		-- ARM_T1_HOV_Skimmer
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
		weaponvelocity = 450,  -- TA 3.1c (was 900)
		-- stats
		range = 210,  -- TA 3.1c (was 315)
		reloadtime = 0.8,  -- TA 3.1c (was 1)
		areaofeffect = 8,
		burstrate = 0.2,  -- TA 3.1c (was unset)
		damage = {
			default = 45,  -- TA 3.1c (was 23)
		},
	},
	armpt_laser = {
		-- TA 3.1c weapon armpt_laser (BOTA used arm_scout_laser for it as well)
		-- used by units
		-- ARM_T1_SEA_Skeeter
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
		weaponvelocity = 400,  -- TA 3.1c (was 900)
		-- stats
		range = 180,  -- TA 3.1c (was 315)
		reloadtime = 1,
		areaofeffect = 8,
		burstrate = 0.2,  -- TA 3.1c (was unset)
		damage = {
			default = 13,  -- TA 3.1c (was 23)
		},
	},
	arm_laser = {
		-- TA 3.1c weapon arm_laser (BOTA used arm_scout_laser for it as well)
		-- used by units
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
		weaponvelocity = 400,  -- TA 3.1c (was 900)
		-- stats
		range = 180,  -- TA 3.1c (was 315)
		reloadtime = 0.865,  -- TA 3.1c (was 1)
		areaofeffect = 8,
		burstrate = 0.2,  -- TA 3.1c (was unset)
		damage = {
			default = 30,  -- TA 3.1c (was 23)
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
		damage = {
			default = 6,  -- TA 3.1c (was 16)
			arm_aircraft = 32,
			core_aircraft = 32,
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
		weaponvelocity = 500,  -- TA 3.1c (was 900)
		-- stats
		range = 260,  -- TA 3.1c (was 360)
		reloadtime = 1.6,  -- TA 3.1c (was 0.9)
		areaofeffect = 8,
		damage = {
			default = 60,  -- TA 3.1c (was 70)
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
		weaponvelocity = 400,  -- TA 3.1c (was 900)
		-- stats
		range = 210,  -- TA 3.1c (was 367)
		reloadtime = 0.8,
		areaofeffect = 8,
		burstrate = 0.2,  -- TA 3.1c (was unset)
		damage = {
			default = 40,  -- TA 3.1c (was 46)
		},
	},
}
