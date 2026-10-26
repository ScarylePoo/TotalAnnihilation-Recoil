-- CORE_T1_DEF_Mine2 (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_def_mine2 = {
		-- id
		name = "M-303",
		description = "Land Mine",
		side = "CORE",
		unitname = "core_t1_def_mine2",
		objectname = "CORE_T1_DEF_Mine2.s3o",
		script = "CORE_T1_DEF_Mine2.lua",
		category = "CORE MINE LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1204,
		buildcostmetal = 32,
		buildtime = 2130,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 15,
		-- combat
		firestate = 2,
		kamikaze = 1,
		kamikazedistance = 40,
		selfdestructcountdown = 1,
		explodeas = "CORMINE2",
		selfdestructas = "CORMINE2",
		-- properties
		maxdamage = 32,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 55,
		-- other abilities
		stealth = 1,
		cloakcost = 2,
		mincloakdistance = 10,
		-- unit animation
		footprintx = 1,
		footprintz = 1,
		yardmap = "o",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		defaultmissiontype = "Standby_Mine",
		initcloaked = 1,
		sounds = {
			arrived = {
				"servsml6",
			},
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			ok = {
				"servsml6",
			},
			select = {
				"minesel2",
			},
			underattack = "warning1",
		},
	},
}
