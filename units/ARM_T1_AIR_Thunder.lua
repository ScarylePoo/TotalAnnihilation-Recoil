-- ARM_T1_AIR_Thunder (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_air_thunder = {
		-- id
		name = "Thunder",
		description = "Bomber",
		side = "ARM",
		unitname = "arm_t1_air_thunder",
		objectname = "ARM_T1_AIR_Thunder",
		corpse = "ARM_T1_AIR_Thunder_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL1 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5496,
		buildcostmetal = 130,
		buildtime = 10155,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 200,
		maxvelocity = 10,
		brakerate = 1.3,
		acceleration = 0.08,
		turnrate = 356,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		nochasecategory = "UNDERWATER",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 320,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 512,
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
		attackrunlength = 120,
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
		weapons = {
			{
				name = "ARM_THUNDER_BOMB",
			},
		},
	},
}
