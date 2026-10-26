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
		corpse = "CORE_T2_AIR_AdvancedConstructor_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL2 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 14824,
		buildcostmetal = 831,
		buildtime = 22001,
		energymake = 5,
		metalmake = 0.1,
		energystorage = 100,
		metalstorage = 100,
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
		turnrate = 250,
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 110,
		builddistance = 128,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 370,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 516,
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
