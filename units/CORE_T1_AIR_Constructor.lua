-- CORE_T1_AIR_Constructor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_air_constructor = {
		-- id
		name = "Construction Aircraft",
		description = "Tech Level 1",
		side = "CORE",
		unitname = "core_t1_air_constructor",
		buildoptions = Shared.buildListCoreT1AircraftConstructor,
		objectname = "CORE_T1_AIR_Constructor",
		corpse = "CORE_T1_AIR_Constructor_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL1 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4580,
		buildcostmetal = 274,
		buildtime = 7986,
		energystorage = 50,
		metalstorage = 50,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 75,
		maxvelocity = 6.8,
		brakerate = 1.7,
		acceleration = 0.06,
		turnrate = 192,
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 55,
		builddistance = 128,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 290,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 272,
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
