-- ARM_T2_BOT_FARK (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_fark = {
		-- id
		name = "FARK",
		description = "Fast Assist-Repair Kbot",
		side = "ARM",
		unitname = "arm_t2_bot_fark",
		objectname = "ARM_T2_BOT_FARK.s3o",
		buildpic = "ARM_T2_BOT_FARK.png",
		script = "ARM_T2_BOT_FARK.lua",
		corpse = "ARM_T2_BOT_FARK_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3219,  -- TA 3.1c (was 7019)
		buildcostmetal = 480,  -- TA 3.1c (was 626)
		buildtime = 7931,  -- TA 3.1c (was 16831)
		energystorage = 0,  -- TA 3.1c (was 100)
		metalstorage = 0,  -- TA 3.1c (was 100)
		energymake = 17,  -- TA 3.1c (was unset)
		metalmake = 0.5,  -- TA 3.1c (was unset)
		energyuse = 0.4,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.1,  -- TA 3.1c (was 2.6)
		brakerate = 0.6,
		acceleration = 0.18,  -- TA 3.1c (was 0.22)
		turnrate = 1010,
		-- nanolathing
		builder = 1,
		workertime = 180,  -- TA 3.1c (was 130)
		builddistance = 60,  -- TA 3.1c (was 128)
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 830,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 290,  -- TA 3.1c (was 507)
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
