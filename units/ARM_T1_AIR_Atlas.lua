-- ARM_T1_AIR_Atlas (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_air_atlas = {
		-- id
		name = "Atlas",
		description = "VTOL Transport",
		side = "ARM",
		unitname = "arm_t1_air_atlas",
		objectname = "ARM_T1_AIR_Atlas.s3o",
		corpse = "ARM_T1_AIR_Atlas_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL1 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2479,
		buildcostmetal = 107,
		buildtime = 5500,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 90,
		maxvelocity = 8,
		brakerate = 3,
		acceleration = 0.2,
		turnrate = 288,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 210,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 225,
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
		maneuverleashlength = 1280,
		shootme = 1,
		defaultmissiontype = "VTOL_standby",
		ovradjust = 1,
		steeringmode = 1,
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
