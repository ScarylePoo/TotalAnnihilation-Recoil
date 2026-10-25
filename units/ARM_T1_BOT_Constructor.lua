-- ARM_T1_BOT_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_bot_constructor = {
		-- id
		name = "Construction KBot",
		description = "Tech Level 1",
		side = "ARM",
		unitname = "arm_t1_bot_constructor",
		buildoptions = Shared.buildListArmT1KbotConstructor,
		objectname = "ARM_T1_BOT_Constructor.s3o",
		script = "ARM_T1_BOT_Constructor.lua",          -- walker: Lua script on the standard skeleton (was the COB)
		corpse = "ARM_T1_BOT_Constructor_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1610,
		buildcostmetal = 213,
		buildtime = 6197,
		energystorage = 50,
		metalstorage = 50,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.4,
		brakerate = 0.24,
		acceleration = 0.18,
		turnrate = 1020,
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
		maxdamage = 700,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 241,
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
