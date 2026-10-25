-- CORE_T2_SEA_Hive (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_sea_hive = {
		-- id
		name = "Hive",
		description = "Light Carrier",
		side = "CORE",
		unitname = "core_t2_sea_hive",
		objectname = "CORE_T2_SEA_Hive",
		corpse = "CORE_T2_SEA_Hive_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 11715,
		buildcostmetal = 1379,
		buildtime = 25271,
		energymake = 380,
		-- movement or placement
		movementclass = "BIG_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.2,
		brakerate = 0.02,
		acceleration = 0.02,
		turnrate = 128,
		-- nanolathing
		builder = 1,
		workertime = 800,
		canassist = 0,
		canreclaim = 0,
		-- combat
		explodeas = "CRAWL_BLAST",
		selfdestructas = "CRAWL_BLAST",
		-- properties
		maxdamage = 3500,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		radardistance = 2400,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		isairbase = 1,
		-- unit animation
		footprintx = 8,
		footprintz = 8,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		buildangle = 16384,
		ovradjust = 1,
		sounds = {
			arrived = {
				"shcorstp",
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
				"shcormov",
			},
			select = {
				"shcorsel",
			},
			underattack = "warning1",
		},
	},
}
