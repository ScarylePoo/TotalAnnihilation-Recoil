-- CORE_T1_BOT_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_bot_constructor = {
		-- id
		name = "Construction Kbot",
		description = "Tech Level 1",
		side = "CORE",
		unitname = "core_t1_bot_constructor",
		buildoptions = Shared.buildListCoreT1KbotConstructor,
		objectname = "CORE_T1_BOT_Constructor",
		corpse = "CORE_T1_BOT_Constructor_dead",
		icontype = "kbot",
		category = "CORE KBOT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1540,
		buildcostmetal = 189,
		buildtime = 6518,
		energystorage = 50,
		metalstorage = 50,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.55,
		brakerate = 0.2,
		acceleration = 0.11,
		turnrate = 965,
		maxwaterdepth = 25,
		maxslope = 20,
		-- nanolathing
		builder = 1,
		workertime = 65,
		builddistance = 128,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 710,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 235,
		-- unit animation
		upright = 1,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 22,
		trackoffset = 0,
		trackstrength = 5,
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
		ovradjust = 1,
		sounds = {
			arrived = {
				"kbcorstp",
			},
			build = "nanlath2",
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
			repair = "repair2",
			select = {
				"kbcorsel",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
