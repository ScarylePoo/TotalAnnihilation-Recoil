-- CORE_T2_BOT_Roach (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_roach = {
		-- id
		name = "Roach",
		description = "Crawling Bomb",
		side = "CORE",
		unitname = "core_t2_bot_roach",
		objectname = "CORE_T2_BOT_Roach",
		icontype = "kbot",
		category = "CORE KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5471,
		buildcostmetal = 65,
		buildtime = 7899,
		-- movement or placement
		movementclass = "CRAWLING_BOMB",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.4,
		brakerate = 0.12,
		acceleration = 0.1,
		turnrate = 1370,
		maxwaterdepth = 112,
		maxslope = 32,
		-- combat
		kamikaze = 1,
		kamikazedistance = 80,
		selfdestructcountdown = 1,
		explodeas = "CRAWL_BLASTEX",
		selfdestructas = "CRAWL_BLAST",
		-- properties
		maxdamage = 195,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 175,
		-- unit animation
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 13,
		trackoffset = 0,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "SpidTrack",
		footprintx = 1,
		footprintz = 1,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		ovradjust = 1,
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
				"servsml6",
			},
			underattack = "warning1",
		},
	},
}
