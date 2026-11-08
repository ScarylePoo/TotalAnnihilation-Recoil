-- ARM_T1_HOV_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_hov_constructor = {
		-- id
		name = "Construction Hovercraft",
		description = "Tech Level 1",
		side = "ARM",
		unitname = "arm_t1_hov_constructor",
		buildoptions = Shared.buildListArmT1AmphibiousConstructor,
		objectname = "ARM_T1_HOV_Constructor.s3o",
		buildpic = "ARM_T1_HOV_Constructor.png",
		script = "ARM_T1_HOV_Constructor.lua",
		corpse = "ARM_T1_HOV_Constructor_dead",
		icontype = "hover",
		category = "ARM HOVER LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4370,  -- TA 3.1c (was 4870)
		buildcostmetal = 396,  -- TA 3.1c (was 356)
		buildtime = 10494,  -- TA 3.1c (was 12394)
		energystorage = 80,  -- TA 3.1c (was 50)
		metalstorage = 50,
		energymake = 16,  -- TA 3.1c (was unset)
		metalmake = 0.3,  -- TA 3.1c (was unset)
		energyuse = 1,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "TANKHOVER3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canhover = 1,
		maxvelocity = 2.2,
		brakerate = 0.006,  -- TA 3.1c (was 0.06)
		acceleration = 0.01,
		turnrate = 120,
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
		maxdamage = 723,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 270,  -- TA 3.1c (was 470)
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
				"hovmdof1",
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
				"hovmdok1",
			},
			repair = "repair1",
			select = {
				"hovmdsl1",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
