-- ARM_T1_SEA_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_sea_constructor = {
		-- id
		name = "Construction Ship",
		description = "Tech Level 1",
		side = "ARM",
		unitname = "arm_t1_sea_constructor",
		buildoptions = Shared.buildListArmT1SeaConstructor,
		objectname = "ARM_T1_SEA_Constructor.s3o",
		buildpic = "ARM_T1_SEA_Constructor.png",
		script = "ARM_T1_SEA_Constructor.lua",
		corpse = "ARM_T1_SEA_Constructor_dead",
		icontype = "ship",
		category = "ARM SHIP LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2130,
		buildcostmetal = 255,  -- TA 3.1c (was 285)
		buildtime = 5121,  -- TA 3.1c (was 5421)
		energystorage = 50,
		metalstorage = 50,
		energymake = 7,  -- TA 3.1c (was unset)
		metalmake = 0.3,  -- TA 3.1c (was unset)
		energyuse = 0.1,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "SMALL_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.1,
		brakerate = 0.04,
		acceleration = 0.009,  -- TA 3.1c (was 0.01)
		turnrate = 200,
		-- nanolathing
		builder = 1,
		workertime = 125,  -- TA 3.1c (was 70)
		builddistance = 60,  -- TA 3.1c (was 128)
		-- combat
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 1105,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 224,  -- TA 3.1c (was 392)
		-- unit animation
		waterline = 4,
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
				"sharmstp",
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
				"sharmmov",
			},
			repair = "repair1",
			select = {
				"sharmsel",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
