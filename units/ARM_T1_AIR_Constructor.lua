-- ARM_T1_AIR_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_air_constructor = {
		-- id
		name = "Construction Aircraft",
		description = "Tech Level 1",
		side = "ARM",
		unitname = "arm_t1_air_constructor",
		buildoptions = Shared.buildListArmT1AircraftConstructor,
		objectname = "ARM_T1_AIR_Constructor.s3o",
		corpse = "ARM_T1_AIR_Constructor_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL1 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4320,
		buildcostmetal = 275,
		buildtime = 8844,
		energystorage = 50,
		metalstorage = 50,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 70,
		maxvelocity = 6.9,
		brakerate = 1.5,
		acceleration = 0.09,
		turnrate = 180,
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 55,
		builddistance = 128,
		-- combat
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 280,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 290,
		-- unit animation
		collide = 1,
		footprintx = 3,
		footprintz = 3,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "VTOL_standby",
		maneuverleashlength = 1280,
		ovradjust = 1,
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
