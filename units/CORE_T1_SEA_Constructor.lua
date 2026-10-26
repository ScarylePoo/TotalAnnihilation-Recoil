-- CORE_T1_SEA_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_sea_constructor = {
		-- id
		name = "Construction Ship",
		description = "Tech Level 1",
		side = "CORE",
		unitname = "core_t1_sea_constructor",
		buildoptions = Shared.buildListCoreT1SeaConstructor,
		objectname = "CORE_T1_SEA_Constructor.s3o",
		corpse = "CORE_T1_SEA_Constructor_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2375,
		buildcostmetal = 275,
		buildtime = 5537,
		energystorage = 50,
		metalstorage = 50,
		-- movement or placement
		movementclass = "SMALL_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.1,
		brakerate = 0.042,
		acceleration = 0.008,
		turnrate = 205,
		-- nanolathing
		builder = 1,
		workertime = 70,
		builddistance = 128,
		-- combat
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 1150,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 377,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
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
				"shcorstp",
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
				"shcormov",
			},
			repair = "repair2",
			select = {
				"shcorsel",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
