-- Weapon definitions (converted from BOTA_CORE_Lasers.TDF)

return {
	core_scout_laser = {
		-- used by units
		-- CORE_T1_HOV_Scrubber
		-- CORE_T1_VEH_Weasel
		-- CORE_T1_SEA_Searcher
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		tolerance = 500,
		-- visuals
		loddistance = 4000,
		duration = 0.06,
		hardstop = 1,
		thickness = 7,
		rgbcolor = "0.6 0.3 0",  -- orange
		corethickness = 0.3,
		rgbcolor2 = "0.9 0.4 0",  -- even more orange
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrfir1",
		soundhit = "lasrhit2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		weaponvelocity = 800,
		-- stats
		range = 305,
		reloadtime = 0.8,
		areaofeffect = 8,
		damage = {
			default = 18,
		},
	},
	core_hurricane_laser = {
		-- used by units
		-- CORE_T2_AIR_Hurricane
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		-- visuals
		loddistance = 4000,
		duration = 0.04,
		hardstop = 1,
		thickness = 6,
		rgbcolor = "0.6 0.2 0",  -- red-orange
		corethickness = 0.3,
		rgbcolor2 = "0.9 0.3 0",  -- red-orange
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrlit1",
		soundhit = "lashit",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		weaponvelocity = 800,
		-- stats
		range = 600,
		reloadtime = 0.39,
		areaofeffect = 8,
		damage = {
			default = 15,
		},
	},
	core_laser = {
		-- used by units
		-- CORE_T1_BOT_Ak
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		-- visuals
		loddistance = 4000,
		duration = 0.02,
		hardstop = 1,
		thickness = 2,
		rgbcolor = "0.8 0 0",  -- reddish
		corethickness = 0.5,
		rgbcolor2 = "0.9 0.4 0.4",  -- white-reddish
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrfir1",
		soundhit = "lasrhit2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		weaponvelocity = 800,
		-- stats
		range = 271,
		reloadtime = 0.7,
		areaofeffect = 8,
		damage = {
			default = 44,
		},
	},
	gator_laser = {
		-- used by units
		-- CORE_T1_VEH_Instigator
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		-- visuals
		loddistance = 4000,
		duration = 0.02,
		hardstop = 1,
		thickness = 2,
		rgbcolor = "0.8 0 0",  -- reddish
		corethickness = 0.5,
		rgbcolor2 = "0.9 0.4 0.4",  -- white-reddish
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrlit3",
		soundhit = "lasrhit2",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		weaponvelocity = 800,
		-- stats
		range = 270,
		reloadtime = 1,
		areaofeffect = 8,
		damage = {
			default = 70,
		},
	},
	corfast_weapon = {
		-- used by units
		-- CORE_T2_BOT_Freaker
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		-- visuals
		loddistance = 4000,
		duration = 0.02,
		hardstop = 1,
		thickness = 3,
		rgbcolor = "0.8 0 0",  -- reddish
		corethickness = 0.5,
		rgbcolor2 = "0.9 0.4 0.4",  -- white-reddish
		-- sounds
		soundtrigger = 1,
		soundstart = "lasrfast",
		soundhit = "lashit",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 50,
		tolerance = 1000,
		weaponvelocity = 800,
		-- stats
		range = 315,
		reloadtime = 0.6,
		areaofeffect = 8,
		damage = {
			default = 57,
		},
	},
	coramph_weapon2 = {
		-- used by units
		-- CORE_T2_BOT_Gimp
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		-- visuals
		loddistance = 4000,
		duration = 0.15,
		hardstop = 1,
		thickness = 10,
		rgbcolor = "0 0.8 0",  -- greenish
		corethickness = 0.5,
		rgbcolor2 = "0.4 0.9 4",  -- green-whiteish
		-- sounds
		soundstart = "lasrhvy3",
		soundhit = "lasrhit1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 90,
		tolerance = 300,
		weaponvelocity = 700,
		-- costs
		energypershot = 100,
		-- stats
		range = 525,
		reloadtime = 1.05,
		areaofeffect = 12,
		damage = {
			default = 90,
		},
	},
	corsumo_weapon = {
		-- used by units
		-- CORE_T2_BOT_Sumo
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		-- visuals
		loddistance = 4000,
		duration = 0.15,
		hardstop = 1,
		thickness = 12,
		rgbcolor = "0 0.8 0",  -- greenish
		corethickness = 0.5,
		rgbcolor2 = "0.4 0.9 4",  -- green-whiteish
		-- sounds
		soundstart = "lasrhvy3",
		soundhit = "lasrhit1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 90,
		weaponvelocity = 700,
		-- costs
		energypershot = 100,
		-- stats
		range = 600,
		reloadtime = 1.05,
		areaofeffect = 19,
		damage = {
			default = 330,
		},
	},
	core_canlaser = {
		-- used by units
		-- CORE_T2_BOT_TheCan
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		-- visuals
		loddistance = 4000,
		duration = 0.15,
		hardstop = 1,
		thickness = 10,
		rgbcolor = "0 0.8 0",  -- greenish
		corethickness = 0.5,
		rgbcolor2 = "0.4 0.9 4",  -- green-whiteish
		-- sounds
		soundstart = "lasrhvy3",
		soundhit = "lasrhit1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 90,
		weaponvelocity = 700,
		-- costs
		energypershot = 75,
		-- stats
		range = 520,
		reloadtime = 0.95,
		areaofeffect = 18,
		damage = {
			default = 220,
		},
	},
	core_batslaser = {
		-- used by units
		-- CORE_T2_SEA_Warlord
		-- type
		weapontype = "LaserCannon",
		turret = 1,
		-- visuals
		duration = 0.15,
		hardstop = 1,
		thickness = 10,
		rgbcolor = "0 0.8 0",  -- greenish
		corethickness = 0.5,
		rgbcolor2 = "0.4 0.9 4",  -- green-whiteish
		-- sounds
		soundstart = "Lasrmas2",
		soundhit = "lasrhit1",
		-- behaviour
		avoidfriendly = 0,
		collidefriendly = 0,
		firestarter = 90,
		tolerance = 500,
		weaponvelocity = 700,
		-- costs
		energypershot = 75,
		-- stats
		range = 810,
		reloadtime = 1.1,
		areaofeffect = 8,
		damage = {
			default = 159,
		},
	},
}
