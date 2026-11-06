-- CORE_T1_DEF_Mine6 (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_def_mine6 = {
		-- id
		name = "M-610",
		description = "Nuclear Mine",
		side = "CORE",
		unitname = "core_t1_def_mine6",
		objectname = "CORE_T1_DEF_Mine6.s3o",
		buildpic = "CORE_T1_DEF_Mine6.png",
		script = "CORE_T1_DEF_Mine6.lua",
		category = "CORE MINE LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 26172,  -- TA 3.1c (was 25172)
		buildcostmetal = 595,  -- TA 3.1c (was 545)
		buildtime = 32715,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 15,
		-- combat
		firestate = 2,
		kamikaze = 1,
		kamikazedistance = 64,
		selfdestructcountdown = 2,
		explodeas = "CORMINE6",
		selfdestructas = "CORMINE6",
		-- properties
		maxdamage = 200,  -- TA 3.1c (was 50)
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 90,
		-- other abilities
		stealth = 1,
		cloakcost = 123,  -- TA 3.1c (was 40)
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
				"minesel4",
			},
			underattack = "warning1",
		},
	},
}
