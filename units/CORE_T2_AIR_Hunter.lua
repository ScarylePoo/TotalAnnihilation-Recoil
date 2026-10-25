-- CORE_T2_AIR_Hunter (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_air_hunter = {
		-- id
		name = "Hunter",
		description = "Airborne Sonar",
		side = "CORE",
		unitname = "core_t2_air_hunter",
		objectname = "CORE_T2_AIR_Hunter",
		corpse = "CORE_T2_AIR_Hunter_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL2 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7421,
		buildcostmetal = 142,
		buildtime = 10512,
		energyuse = 15,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 190,
		maxvelocity = 9.7,
		brakerate = 3,
		acceleration = 0.05,
		turnrate = 409,
		maxwaterdepth = 255,
		maxslope = 10,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 515,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		sonardistance = 1445,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		collide = 0,
		footprintx = 3,
		footprintz = 3,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "VTOL_standby",
		maneuverleashlength = 1280,
		altfromsealevel = 1,
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
				"vtolcrmv",
			},
			repair = "repair1",
			select = {
				"seasonr2",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
