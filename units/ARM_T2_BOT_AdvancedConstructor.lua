-- ARM_T2_BOT_AdvancedConstructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_advancedconstructor = {
		-- id
		name = "Adv. Construction Kbot",
		description = "Tech Level 2",
		side = "ARM",
		unitname = "arm_t2_bot_advancedconstructor",
		buildoptions = Shared.buildListArmT2KbotConstructor,
		objectname = "ARM_T2_BOT_AdvancedConstructor.s3o",
		script = "ARM_T2_BOT_AdvancedConstructor.lua",
		corpse = "ARM_T2_BOT_AdvancedConstructor_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7784,
		buildcostmetal = 697,
		buildtime = 18432,
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
		brakerate = 0.6,
		acceleration = 0.18,
		turnrate = 1010,
		-- nanolathing
		builder = 1,
		workertime = 130,
		builddistance = 128,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1040,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 435,
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
				"kbarmstp",
			},
			build = "nanlath1",
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
			repair = "repair1",
			select = {
				"kbarmsel",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
