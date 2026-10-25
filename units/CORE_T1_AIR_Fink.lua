-- CORE_T1_AIR_Fink (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_air_fink = {
		-- id
		name = "Fink",
		description = "Air Scout",
		side = "CORE",
		unitname = "core_t1_air_fink",
		objectname = "CORE_T1_AIR_Fink",
		corpse = "CORE_T1_AIR_Fink_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL1 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1369,
		buildcostmetal = 36,
		buildtime = 2156,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 200,
		maxvelocity = 11,
		brakerate = 10,
		acceleration = 0.4,
		turnrate = 700,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 90,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 725,
		radardistance = 1224,
		-- unit animation
		collide = 0,
		footprintx = 2,
		footprintz = 2,
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
