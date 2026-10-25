-- CORE_T2_BOT_Freaker (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_freaker = {
		-- id
		name = "Freaker",
		description = "Fast Attack Kbot",
		side = "CORE",
		unitname = "core_t2_bot_freaker",
		objectname = "CORE_T2_BOT_Freaker",
		corpse = "CORE_T2_BOT_Freaker_dead",
		icontype = "kbot",
		category = "CORE KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2658,
		buildcostmetal = 175,
		buildtime = 8541,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 3.75,
		brakerate = 0.2,
		acceleration = 0.1,
		turnrate = 1111,
		maxwaterdepth = 22,
		maxslope = 17,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 630,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 490,
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
				name = "CORFAST_WEAPON",
			},
		},
	},
}
