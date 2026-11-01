-- ARM_T2_BOT_Infiltrator (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_infiltrator = {
		-- id
		name = "Infiltrator",
		description = "SPY Kbot",
		side = "ARM",
		unitname = "arm_t2_bot_infiltrator",
		objectname = "ARM_T2_BOT_Infiltrator.s3o",
		script = "ARM_T2_BOT_Infiltrator.lua",
		corpse = "ARM_T2_BOT_Infiltrator_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 9219,
		buildcostmetal = 128,
		buildtime = 22631,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.1,
		brakerate = 0.15,
		acceleration = 0.2,
		turnrate = 1016,
		maxwaterdepth = 12,
		maxslope = 24,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 270,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 490,
		-- other abilities
		stealth = 1,
		cloakcost = 120,
		cloakcostmoving = 400,
		mincloakdistance = 40,
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
				"kbarmstp",
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
				"kbarmmov",
			},
			select = {
				"kbarmsel",
			},
			underattack = "warning1",
		},
	},
}
