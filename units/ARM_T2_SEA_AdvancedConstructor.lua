-- ARM_T2_SEA_AdvancedConstructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_sea_advancedconstructor = {
		-- id
		name = "Advanced Construction Sub",
		description = "Tech Level 2",
		side = "ARM",
		unitname = "arm_t2_sea_advancedconstructor",
		buildoptions = Shared.buildListArmT2SeaConstructor,
		objectname = "ARM_T2_SEA_AdvancedConstructor.s3o",
		buildpic = "ARM_T2_SEA_AdvancedConstructor.png",
		script = "ARM_T2_SEA_AdvancedConstructor.lua",
		corpse = "ARM_T2_SEA_AdvancedConstructor_dead",
		icontype = "ship",
		category = "ARM UNDERWATER LEVEL2 NOWEAPON NOTAIR",
		-- costs, makes, uses, storage
		buildcostenergy = 7568,  -- TA 3.1c (was 8568)
		buildcostmetal = 695,  -- TA 3.1c (was 865)
		buildtime = 16565,  -- TA 3.1c (was 17265)
		energymake = 17,  -- TA 3.1c (was 5)
		metalmake = 0.9,  -- TA 3.1c (was 0.1)
		energystorage = 50,  -- TA 3.1c (was 100)
		metalstorage = 50,  -- TA 3.1c (was 100)
		energyuse = 0.1,  -- TA 3.1c (was unset)
		sonardistance = 400,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "SHIP_SUBMARINE",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.15,
		brakerate = 0.2,
		acceleration = 0.032,  -- TA 3.1c (was 0.03)
		turnrate = 256,
		-- nanolathing
		builder = 1,
		workertime = 225,  -- TA 3.1c (was 140)
		builddistance = 100,  -- TA 3.1c (was 128)
		-- combat
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 360,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 120,  -- TA 3.1c (was 210)
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
				"suarmstp",
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
				"suarmmov",
			},
			repair = "repair1",
			select = {
				"suarmsel",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
