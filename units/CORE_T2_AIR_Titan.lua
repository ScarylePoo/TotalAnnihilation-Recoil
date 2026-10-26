-- CORE_T2_AIR_Titan (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_air_titan = {
		-- id
		name = "Titan",
		description = "Torpedo Bomber",
		side = "CORE",
		unitname = "core_t2_air_titan",
		objectname = "CORE_T2_AIR_Titan.s3o",
		corpse = "CORE_T2_AIR_Titan_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL2 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 6588,
		buildcostmetal = 364,
		buildtime = 13722,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 150,
		maxvelocity = 9.5,
		brakerate = 5,
		acceleration = 0.15,
		turnrate = 409,
		maxwaterdepth = 255,
		maxslope = 10,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 375,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
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
		weapons = {
			{
				name = "CORAIR_TORPEDO",
			},
		},
	},
}
