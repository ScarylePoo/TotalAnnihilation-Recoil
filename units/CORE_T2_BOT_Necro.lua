-- CORE_T2_BOT_Necro (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_necro = {
		-- id
		name = "Necro",
		description = "Resurrection Kbot",
		side = "CORE",
		unitname = "core_t2_bot_necro",
		objectname = "CORE_T2_BOT_Necro.s3o",
		buildpic = "CORE_T2_BOT_Necro.png",
		script = "CORE_T2_BOT_Necro.lua",
		corpse = "CORE_T2_BOT_Necro_dead",
		category = "CORE KBOT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 10164,
		buildcostmetal = 376,  -- TA 3.1c (was 626)
		buildtime = 11416,  -- TA 3.1c (was 15416)
		energystorage = 50,  -- TA 3.1c (was 100)
		metalstorage = 50,  -- TA 3.1c (was 100)
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.4,  -- TA 3.1c (was 1.7)
		brakerate = 0.15,
		acceleration = 0.1,
		turnrate = 1016,
		-- nanolathing
		builder = 1,
		workertime = 160,  -- TA 3.1c (was 100)
		builddistance = 30,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 470,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 290,  -- TA 3.1c (was 508)
		-- other abilities
		stealth = 1,
		canresurrect = 1,
		resurrectspeed = 200,
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
				"necrnan2",
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
				"necrok2",
			},
			select = {
				"necrsel2",
			},
			underattack = "warning1",
		},
	},
}
