-- CORE_T1_SEAPL_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seapl_constructor = {
		-- id
		name = "Construction Seaplane",
		description = "Tech Level 1",
		side = "CORE",
		unitname = "core_t1_seapl_constructor",
		buildoptions = Shared.buildListCoreT1SeaplaneConstructor,
		objectname = "CORE_T1_SEAPL_Constructor",
		corpse = "CORE_T1_SEAPL_Constructor_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL1 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5824,
		buildcostmetal = 425,
		buildtime = 11520,
		energystorage = 50,
		metalstorage = 50,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 75,
		maxvelocity = 6.3,
		brakerate = 1.7,
		acceleration = 0.04,
		turnrate = 116,
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
		idleautoheal = .5,
		sightdistance = 472,
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
		amphibious = 1,
		cansubmerge = 1,
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
