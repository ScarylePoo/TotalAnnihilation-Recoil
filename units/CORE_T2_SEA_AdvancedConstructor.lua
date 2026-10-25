-- CORE_T2_SEA_AdvancedConstructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_sea_advancedconstructor = {
		-- id
		name = "Advanced Construction Sub",
		description = "Tech Level 2",
		side = "CORE",
		unitname = "core_t2_sea_advancedconstructor",
		buildoptions = Shared.buildListCoreT2SeaConstructor,
		objectname = "CORE_T2_SEA_AdvancedConstructor",
		corpse = "CORE_T2_SEA_AdvancedConstructor_dead",
		icontype = "ship",
		category = "CORE UNDERWATER LEVEL2 NOWEAPON NOTAIR",
		-- costs, makes, uses, storage
		buildcostenergy = 7911,
		buildcostmetal = 864,
		buildtime = 17228,
		energymake = 5,
		metalmake = 0.1,
		energystorage = 100,
		metalstorage = 100,
		-- movement or placement
		movementclass = "SHIP_SUBMARINE",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.05,
		brakerate = 0.2,
		acceleration = 0.04,
		turnrate = 256,
		-- nanolathing
		builder = 1,
		workertime = 140,
		builddistance = 128,
		-- combat
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 370,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 210,
		-- unit animation
		waterline = 40,
		footprintx = 3,
		footprintz = 3,
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
				"sucorstp",
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
				"sucormov",
			},
			repair = "repair1",
			select = {
				"sucorsel",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
