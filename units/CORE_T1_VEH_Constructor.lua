-- CORE_T1_VEH_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_veh_constructor = {
		-- id
		name = "Construction Vehicle",
		description = "Tech Level 1",
		side = "CORE",
		unitname = "core_t1_veh_constructor",
		buildoptions = Shared.buildListCoreT1VehicleConstructor,
		objectname = "CORE_T1_VEH_Constructor.s3o",
		corpse = "CORE_T1_VEH_Constructor_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1445,
		buildcostmetal = 221,
		buildtime = 7146,
		energystorage = 50,
		metalstorage = 50,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.5,
		brakerate = 0.1,
		acceleration = 0.019,
		turnrate = 207,
		maxwaterdepth = 19,
		maxslope = 16,
		-- nanolathing
		builder = 1,
		workertime = 60,
		builddistance = 128,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 825,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 350,
		-- unit animation
		leavetracks = 1,
		trackwidth = 28,
		trackoffset = 3,
		trackstrength = 5,
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
