-- Weapon definitions (converted from BOTA_CORE_Lasers_for_towers.TDF)

return {
	core_light_laser = {
		-- used by units
		-- CORE_T1_DEF_LightLaserTower
		-- CORE_T2_DEF_DoomsdayMachine
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		tolerance = 700,  -- TA 3.1c (was 500)
		-- visuals
		loddistance = 4000,
		duration = 0.15,
		hardstop = 1,
		thickness = 7,
		rgbcolor = "0.8 0 0",  -- reddish
		corethickness = 0.3,
		rgbcolor2 = "0.9 0.4 0.4",  -- white-reddish
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrfir3",
		soundhit = "lasrhit2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 30,
		weaponvelocity = 800,
		-- costs
		energypershot = 10,
		-- stats
		range = 300,  -- TA 3.1c (was 512)
		reloadtime = 0.52,
		areaofeffect = 8,
		damage = {
			default = 60,  -- TA 3.1c (was 72)
		},
	},
	corvipe_laser = {
		-- TA 3.1c weapon corvipe_laser (BOTA used core_heavy_laser for it as well)
		-- used by units
		-- CORE_T1_DEF_Viper
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		tolerance = 2000,  -- TA 3.1c (was 1000)
		-- visuals
		loddistance = 4000,
		duration = 0.15,
		hardstop = 1,
		thickness = 10,
		rgbcolor = "0 0.8 0",  -- greenish
		corethickness = 0.3,
		rgbcolor2 = "0.4 0.9 4",  -- green-whiteish
		-- sounds
		soundstart = "Lasrmas2",
		soundhit = "lasrhit1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 90,
		weaponvelocity = 800,
		-- costs
		energypershot = 25,  -- TA 3.1c (was 75)
		-- stats
		range = 380,  -- TA 3.1c (was 650)
		reloadtime = 1,  -- TA 3.1c (was 0.965)
		areaofeffect = 8,
		damage = {
			default = 140,  -- TA 3.1c (was 240)
		},
	},
	core_laserh1 = {
		-- TA 3.1c weapon core_laserh1 (BOTA used core_heavy_laser for it as well)
		-- used by units
		-- CORE_T1_DEF_GaatGun
		-- CORE_T2_DEF_DoomsdayMachine
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		tolerance = 500,  -- TA 3.1c (was 1000)
		-- visuals
		loddistance = 4000,
		duration = 0.15,
		hardstop = 1,
		thickness = 10,
		rgbcolor = "0 0.8 0",  -- greenish
		corethickness = 0.3,
		rgbcolor2 = "0.4 0.9 4",  -- green-whiteish
		-- sounds
		soundstart = "Lasrmas2",
		soundhit = "lasrhit1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 90,
		weaponvelocity = 700,  -- TA 3.1c (was 800)
		-- costs
		energypershot = 75,
		-- stats
		range = 400,  -- TA 3.1c (was 650)
		reloadtime = 0.965,
		areaofeffect = 8,
		damage = {
			default = 180,  -- TA 3.1c (was 240)
		},
	},
	core_floating_heavy_laser = {
		-- used by units
		-- CORE_T1_SEADEF_Thunderbolt
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		tolerance = 1000,
		-- visuals
		loddistance = 4000,
		duration = 0.15,
		hardstop = 1,
		thickness = 12,
		rgbcolor = "0 0.8 0",  -- greenish
		corethickness = 0.3,
		rgbcolor2 = "0.4 0.9 4",  -- green-whiteish
		-- sounds
		soundstart = "Lasrmas2",
		soundhit = "lasrhit1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 90,
		weaponvelocity = 700,  -- TA 3.1c (was 800)
		-- costs
		energypershot = 75,  -- TA 3.1c (was 95)
		-- stats
		range = 410,  -- TA 3.1c (was 690)
		reloadtime = 1,
		areaofeffect = 8,
		damage = {
			default = 195,  -- TA 3.1c (was 220)
		},
	},
}
