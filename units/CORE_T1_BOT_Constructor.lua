-- CORE_T1_BOT_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_bot_constructor = {
		-- id
		name = "Construction Kbot",
		description = "Tech Level 1",
		side = "CORE",
		unitname = "core_t1_bot_constructor",
		buildoptions = Shared.buildListCoreT1KbotConstructor,
		objectname = "CORE_T1_BOT_Constructor.s3o",
		buildpic = "CORE_T1_BOT_Constructor.png",
		script = "CORE_T1_BOT_Constructor.lua",          -- walker: Lua script on the standard skeleton (was the COB)
		corpse = "CORE_T1_BOT_Constructor_dead",
		category = "CORE KBOT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2540,  -- TA 3.1c (was 1540)
		buildcostmetal = 130,  -- TA 3.1c (was 189)
		buildtime = 5818,  -- TA 3.1c (was 6518)
		energystorage = 50,
		metalstorage = 50,
		energymake = 8.5,  -- TA 3.1c (was unset)
		metalmake = 0.25,  -- TA 3.1c (was unset)
		energyuse = 0.2,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 0.9,  -- TA 3.1c (was 1.55)
		brakerate = 0.2,
		acceleration = 0.107,  -- TA 3.1c (was 0.11)
		turnrate = 965,
		maxwaterdepth = 25,
		maxslope = 20,
		-- nanolathing
		builder = 1,
		workertime = 80,  -- TA 3.1c (was 65)
		builddistance = 40,  -- TA 3.1c (was 128)
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 710,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 230,  -- TA 3.1c (was 235)
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
