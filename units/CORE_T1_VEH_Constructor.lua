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
		buildpic = "CORE_T1_VEH_Constructor.png",
		script = "CORE_T1_VEH_Constructor.lua",
		corpse = "CORE_T1_VEH_Constructor_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2145,  -- TA 3.1c (was 1445)
		buildcostmetal = 175,  -- TA 3.1c (was 221)
		buildtime = 5146,  -- TA 3.1c (was 7146)
		energystorage = 50,
		metalstorage = 50,
		energymake = 9.2,  -- TA 3.1c (was unset)
		metalmake = 0.25,  -- TA 3.1c (was unset)
		energyuse = 0.2,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.3,  -- TA 3.1c (was 1.5)
		brakerate = 0.085,  -- TA 3.1c (was 0.1)
		acceleration = 0.011,  -- TA 3.1c (was 0.019)
		turnrate = 207,
		maxwaterdepth = 19,
		maxslope = 16,
		-- nanolathing
		builder = 1,
		workertime = 100,  -- TA 3.1c (was 60)
		builddistance = 40,  -- TA 3.1c (was 128)
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 825,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 200,  -- TA 3.1c (was 350)
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
