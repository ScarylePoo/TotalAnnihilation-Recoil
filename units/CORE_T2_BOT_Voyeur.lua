-- CORE_T2_BOT_Voyeur (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_voyeur = {
		-- id
		name = "Voyeur",
		description = "Mobile Radar Kbot",
		side = "CORE",
		unitname = "core_t2_bot_voyeur",
		objectname = "CORE_T2_BOT_Voyeur",
		corpse = "CORE_T2_BOT_Voyeur_dead",
		icontype = "kbot",
		category = "CORE KBOT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1283,
		buildcostmetal = 93,
		buildtime = 3945,
		energyuse = 16,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.2,
		brakerate = 0.012,
		acceleration = 0.041,
		turnrate = 530,
		maxwaterdepth = 0,
		maxslope = 16,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 350,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 420,
		radardistance = 1700,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
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
		steeringmode = 1,
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
