-- CORE_T2_AIR_AdvancedConstructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_air_advancedconstructor = {
		-- id
		name = "Adv. Construction Aircraft",
		description = "Tech Level 2",
		side = "CORE",
		unitname = "core_t2_air_advancedconstructor",
		buildoptions = Shared.buildListCoreT2AircraftConstructor,
		objectname = "CORE_T2_AIR_AdvancedConstructor.s3o",
		buildpic = "CORE_T2_AIR_AdvancedConstructor.png",
		script = "CORE_T2_AIR_AdvancedConstructor.lua",
		corpse = "CORE_T2_AIR_AdvancedConstructor_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL2 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 12824,  -- TA 3.1c (was 14824)
		buildcostmetal = 231,  -- TA 3.1c (was 831)
		buildtime = 26001,  -- TA 3.1c (was 22001)
		energymake = 22,  -- TA 3.1c (was 5)
		metalmake = 0.5,  -- TA 3.1c (was 0.1)
		energystorage = 100,
		metalstorage = 100,
		energyuse = 0.3,  -- TA 3.1c (was unset)
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 70,
		maxvelocity = 7.5,
		brakerate = 1.5,
		acceleration = 0.07,
		turnrate = 130,  -- TA 3.1c (was 250)
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 100,  -- TA 3.1c (was 110)
		builddistance = 60,  -- TA 3.1c (was 128)
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 370,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 295,  -- TA 3.1c (was 516)
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
		defaultmissiontype = "VTOL_Standby",
		maneuverleashlength = 1280,
		ovradjust = 1,
		sounds = {
			arrived = {
				"vtolcrld",
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
				"vtolcrmv",
			},
			repair = "repair2",
			select = {
				"vtolcrac",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
