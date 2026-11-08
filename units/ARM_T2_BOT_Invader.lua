-- ARM_T2_BOT_Invader (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_invader = {
		-- id
		name = "Invader",
		description = "Crawling Bomb",
		side = "ARM",
		unitname = "arm_t2_bot_invader",
		objectname = "ARM_T2_BOT_Invader.s3o",
		buildpic = "ARM_T2_BOT_Invader.png",
		script = "ARM_T2_BOT_Invader.lua",
		icontype = "kbot",
		category = "ARM KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5473,
		buildcostmetal = 61,
		buildtime = 7901,
		-- movement or placement
		movementclass = "CRAWLING_BOMB",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 0.42,  -- TA 3.1c (was 1.5)
		brakerate = 0.13,
		acceleration = 0.11,
		turnrate = 1400,
		maxwaterdepth = 112,
		maxslope = 5,  -- 32
		-- combat
		kamikaze = 1,
		kamikazedistance = 80,
		selfdestructcountdown = 1,
		explodeas = "CRAWL_BLASTSML",
		selfdestructas = "CRAWL_BLAST",
		-- properties
		maxdamage = 185,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 101,  -- TA 3.1c (was 175)
		-- unit animation
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 18,
		trackoffset = 0,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "KbotTrack",
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
				"servsml5",
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
				"servsml5",
			},
			select = {
				"servsml5",
			},
			underattack = "warning1",
		},
	},
}
