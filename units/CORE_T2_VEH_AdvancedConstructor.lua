-- CORE_T2_VEH_AdvancedConstructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_veh_advancedconstructor = {
		-- id
		name = "Adv. Construction Vehicle",
		description = "Tech Level 2",
		side = "CORE",
		unitname = "core_t2_veh_advancedconstructor",
		buildoptions = Shared.buildListCoreT2VehicleConstructor,
		objectname = "CORE_T2_VEH_AdvancedConstructor",
		corpse = "CORE_T2_VEH_AdvancedConstructor_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 8504,
		buildcostmetal = 715,
		buildtime = 20806,
		energymake = 5,
		metalmake = 0.1,
		energystorage = 100,
		metalstorage = 100,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.7,
		brakerate = 0.03,
		acceleration = 0.016,
		turnrate = 210,
		maxwaterdepth = 18,
		maxslope = 16,
		-- nanolathing
		builder = 1,
		workertime = 120,
		builddistance = 128,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1220,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 397,
		-- unit animation
		leavetracks = 1,
		trackwidth = 36,
		trackoffset = 8,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "VehTrack",
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
		ovradjust = 1,
		sounds = {
			arrived = {
				"vcorstop",
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
				"vcormove",
			},
			repair = "repair2",
			select = {
				"vcorsel",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
