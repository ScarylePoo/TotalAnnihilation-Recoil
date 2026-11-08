-- CORE_T2_BOT_Parasite (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_parasite = {
		-- id
		name = "Parasite",
		description = "SPY Kbot",
		side = "CORE",
		unitname = "core_t2_bot_parasite",
		objectname = "CORE_T2_BOT_Parasite.s3o",
		buildpic = "CORE_T2_BOT_Parasite.png",
		script = "CORE_T2_BOT_Parasite.lua",
		corpse = "CORE_T2_BOT_Parasite_dead",
		category = "CORE KBOT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 13452,
		buildcostmetal = 156,
		buildtime = 28247,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.9,  -- TA 3.1c (was 2.1)
		brakerate = 0.15,
		acceleration = 0.2,
		turnrate = 1016,
		maxwaterdepth = 12,
		maxslope = 14,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 340,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 250,
		-- other abilities
		stealth = 1,
		cloakcost = 350,  -- TA 3.1c (was 210)
		cloakcostmoving = 900,  -- TA 3.1c (was 500)
		mincloakdistance = 90,  -- TA 3.1c (was 50)
		-- unit animation
		upright = 1,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 22,
		trackoffset = 0,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "KbotTrack",
		footprintx = 2,
		footprintz = 2,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 2,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		sounds = {
			arrived = {
				"kbcorstp",
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
				"kbcormov",
			},
			select = {
				"kbcorsel",
			},
			underattack = "warning1",
		},
	},
}
