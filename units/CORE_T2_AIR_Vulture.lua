-- CORE_T2_AIR_Vulture (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_air_vulture = {
		-- id
		name = "Vulture",
		description = "Radar Plane",
		side = "CORE",
		unitname = "core_t2_air_vulture",
		objectname = "CORE_T2_AIR_Vulture.s3o",
		corpse = "CORE_T2_AIR_Vulture_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL2 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7824,
		buildcostmetal = 169,
		buildtime = 13264,
		energyuse = 20,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 210,
		maxvelocity = 9.6,
		brakerate = 3,
		acceleration = 0.08,
		turnrate = 365,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 170,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		radardistance = 2100,
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
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "VTOL_standby",
		maneuverleashlength = 1280,
		altfromsealevel = 1,
		sounds = {
			arrived = {
				"vtolcrld",
			},
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
			select = {
				"vtolcrac",
			},
			underattack = "warning1",
		},
	},
}
