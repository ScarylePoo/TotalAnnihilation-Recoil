-- CORE_T2_BOT_AdvancedConstructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_advancedconstructor = {
		-- id
		name = "Adv. Construction Kbot",
		description = "Tech Level 2",
		side = "CORE",
		unitname = "core_t2_bot_advancedconstructor",
		buildoptions = Shared.buildListCoreT2KbotConstructor,
		objectname = "CORE_T2_BOT_AdvancedConstructor",
		corpse = "CORE_T2_BOT_AdvancedConstructor_dead",
		icontype = "kbot",
		category = "CORE KBOT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 9096,
		buildcostmetal = 725,
		buildtime = 19163,
		energymake = 5,
		metalmake = 0.1,
		energystorage = 100,
		metalstorage = 100,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.2,
		brakerate = 0.5,
		acceleration = 0.16,
		turnrate = 1005,
		-- nanolathing
		builder = 1,
		workertime = 130,
		builddistance = 128,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1070,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 429,
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
