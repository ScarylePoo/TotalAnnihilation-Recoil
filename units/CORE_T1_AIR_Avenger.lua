-- CORE_T1_AIR_Avenger (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_air_avenger = {
		-- id
		name = "Avenger",
		description = "Fighter",
		side = "CORE",
		unitname = "core_t1_air_avenger",
		objectname = "CORE_T1_AIR_Avenger",
		corpse = "CORE_T1_AIR_Avenger_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL1 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3181,
		buildcostmetal = 111,
		buildtime = 9196,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 100,
		maxvelocity = 16,
		brakerate = 5,
		acceleration = 0.41,
		turnrate = 805,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 202,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		-- other abilities
		canloopbackattack = 1,
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
		weapons = {
			{
				name = "CORVTOL_MISSILE",
			},
		},
	},
}
