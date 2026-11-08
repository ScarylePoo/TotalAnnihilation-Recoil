-- ARM_T2_VEH_AdvancedConstructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_advancedconstructor = {
		-- id
		name = "Adv. Construction Vehicle",
		description = "Tech Level 2",
		side = "ARM",
		unitname = "arm_t2_veh_advancedconstructor",
		buildoptions = Shared.buildListArmT2VehicleConstructor,
		objectname = "ARM_T2_VEH_AdvancedConstructor.s3o",
		buildpic = "ARM_T2_VEH_AdvancedConstructor.png",
		script = "ARM_T2_VEH_AdvancedConstructor.lua",
		corpse = "ARM_T2_VEH_AdvancedConstructor_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4263,  -- TA 3.1c (was 8263)
		buildcostmetal = 481,  -- TA 3.1c (was 681)
		buildtime = 10397,  -- TA 3.1c (was 20397)
		energymake = 21,  -- TA 3.1c (was 5)
		metalmake = 0.5,  -- TA 3.1c (was 0.1)
		energystorage = 100,
		metalstorage = 100,
		energyuse = 0.1,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.6,
		brakerate = 0.036,
		acceleration = 0.018,
		turnrate = 240,
		maxwaterdepth = 18,
		maxslope = 16,
		-- nanolathing
		builder = 1,
		workertime = 200,  -- TA 3.1c (was 120)
		builddistance = 60,  -- TA 3.1c (was 128)
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1205,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 223,  -- TA 3.1c (was 390)
		-- unit animation
		leavetracks = 1,
		trackwidth = 32,
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
				"varmstop",
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
				"varmmove",
			},
			repair = "repair1",
			select = {
				"varmsel",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
