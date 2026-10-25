-- ARM_T1_SEAPL_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seapl_constructor = {
		-- id
		name = "Construction Seaplane",
		description = "Tech Level 1",
		side = "ARM",
		unitname = "arm_t1_seapl_constructor",
		buildoptions = Shared.buildListArmT1AmphibiousConstructor,
		objectname = "ARM_T1_SEAPL_Constructor",
		corpse = "ARM_T1_SEAPL_Constructor_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL1 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5368,
		buildcostmetal = 395,
		buildtime = 10970,
		energystorage = 50,
		metalstorage = 50,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 70,
		maxvelocity = 6.5,
		brakerate = 1.5,
		acceleration = 0.05,
		turnrate = 120,
		maxwaterdepth = 255,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 55,
		builddistance = 128,
		-- combat
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 200,
		hidedamage = 1,
		idletime = 2200,
		idleaatoheal = .5,
		sightdistance = 490,
		-- other abilities
		cansubmerge = 1,
		-- unit animation
		collide = 1,
		footprintx = 2,
		footprintz = 2,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		scale = 0.8,
		bankscale = 1.5,
		defaultmissiontype = "VTOL_standby",
		maneuverleashlength = 1280,
		ovradjust = 1,
		amphibious = 1,
		sounds = {
			arrived = {
				"vtolarld",
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
				"vtolarmv",
			},
			repair = "repair1",
			select = {
				"vtolarac",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
