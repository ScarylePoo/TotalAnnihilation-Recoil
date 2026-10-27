-- CORE_T2_BOT_Dominator (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_dominator = {
		-- id
		name = "Dominator",
		description = "Heavy Rocket Kbot",
		side = "CORE",
		unitname = "core_t2_bot_dominator",
		objectname = "CORE_T2_BOT_Dominator.s3o",
		script = "CORE_T2_BOT_Dominator.lua",
		corpse = "CORE_T2_BOT_Dominator_dead",
		icontype = "kbot",
		category = "CORE KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2107,
		buildcostmetal = 388,
		buildtime = 5191,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.45,
		brakerate = 0.15,
		acceleration = 0.09,
		turnrate = 1003,
		maxwaterdepth = 21,
		maxslope = 14,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 620,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 500,
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
		weapons = {
			{
				name = "CORE_KBOT_ROCKET",
				onlytargetcategory = "NOTAIR",
			},
		},
	},
}
