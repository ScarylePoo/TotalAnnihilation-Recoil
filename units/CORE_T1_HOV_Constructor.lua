-- CORE_T1_HOV_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_hov_constructor = {
		-- id
		name = "Construction Hovercraft",
		description = "Tech Level 1",
		side = "CORE",
		unitname = "core_t1_hov_constructor",
		buildoptions = Shared.buildListCoreT1HovercraftConstructor,
		objectname = "CORE_T1_HOV_Constructor.s3o",
		buildpic = "CORE_T1_HOV_Constructor.png",
		script = "CORE_T1_HOV_Constructor.lua",
		corpse = "CORE_T1_HOV_Constructor_dead",
		icontype = "hover",
		category = "CORE HOVER LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4455,
		buildcostmetal = 390,
		buildtime = 11028,  -- TA 3.1c (was 12128)
		energystorage = 80,  -- TA 3.1c (was 50)
		metalstorage = 50,
		energymake = 14,  -- TA 3.1c (was unset)
		metalmake = 0.3,  -- TA 3.1c (was unset)
		energyuse = 1,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "TANKHOVER3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canhover = 1,
		maxvelocity = 2.1,  -- TA 3.1c (was 2.3)
		brakerate = 0.008,
		acceleration = 0.01,
		turnrate = 110,
		maxwaterdepth = 0,
		maxslope = 16,
		-- nanolathing
		builder = 1,
		workertime = 80,  -- TA 3.1c (was 65)
		builddistance = 70,  -- TA 3.1c (was 128)
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 740,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 260,  -- TA 3.1c (was 455)
		-- unit animation
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
				"hovmdof2",
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
				"hovmdok2",
			},
			repair = "repair1",
			select = {
				"hovmdsl2",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
