-- CORE_T1_AIR_Avenger (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_air_avenger = {
		-- id
		name = "Avenger",
		description = "Fighter",
		side = "CORE",
		unitname = "core_t1_air_avenger",
		objectname = "CORE_T1_AIR_Avenger.s3o",
		buildpic = "CORE_T1_AIR_Avenger.png",
		script = "CORE_T1_AIR_Avenger.lua",
		corpse = "CORE_T1_AIR_Avenger_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL1 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3181,
		buildcostmetal = 101,  -- TA 3.1c (was 111)
		buildtime = 9196,
		energymake = 0.08,  -- TA 3.1c (was unset)
		energyuse = 0.8,  -- TA 3.1c (was unset)
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 100,
		maxvelocity = 11,  -- TA 3.1c (was 16)
		brakerate = 2,  -- TA 3.1c (was 5)
		acceleration = 0.21,  -- TA 3.1c (was 0.41)
		turnrate = 405,  -- TA 3.1c (was 805)
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 202,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 350,  -- TA 3.1c (was 612)
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
