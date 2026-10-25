-- ARM_T1_AIR_Peeper (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_air_peeper = {
		-- id
		name = "Peeper",
		description = "Air Scout",
		side = "ARM",
		unitname = "arm_t1_air_peeper",
		objectname = "ARM_T1_AIR_Peeper",
		corpse = "ARM_T1_AIR_Peeper_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL1 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1475,
		buildcostmetal = 40,
		buildtime = 2485,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 180,
		maxvelocity = 12,
		brakerate = 9,
		acceleration = 0.5,
		turnrate = 800,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 80,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 750,
		radardistance = 1300,
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
				"vtolarld",
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
				"vtolarmv",
			},
			select = {
				"vtolarac",
			},
			underattack = "warning1",
		},
	},
}
