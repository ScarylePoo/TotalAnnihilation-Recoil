-- CORE_T1_AIR_Valkyrie (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_air_valkyrie = {
		-- id
		name = "Valkyrie",
		description = "VTOL Transport",
		side = "CORE",
		unitname = "core_t1_air_valkyrie",
		objectname = "CORE_T1_AIR_Valkyrie.s3o",
		corpse = "CORE_T1_AIR_Valkyrie_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL1 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2695,
		buildcostmetal = 115,
		buildtime = 5889,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 80,
		maxvelocity = 9.2,
		brakerate = 4,
		acceleration = 0.2,
		turnrate = 245,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 230,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 210,
		-- other abilities
		canload = 1,
		transportsize = 3,
		transportcapacity = 1,
		transportmass = 3000,
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
		ovradjust = 1,
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
