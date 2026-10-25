-- ARM_T1_SEAPL_Tornado (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seapl_tornado = {
		-- id
		name = "Tornado",
		description = "Seaplane Fighter",
		side = "ARM",
		unitname = "arm_t1_seapl_tornado",
		objectname = "ARM_T1_SEAPL_Tornado",
		corpse = "ARM_T1_SEAPL_Tornado_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL1 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 6307,
		buildcostmetal = 237,
		buildtime = 14333,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 100,
		maxvelocity = 14.2,
		brakerate = 5,
		acceleration = 0.5,
		turnrate = 682,
		maxwaterdepth = 255,
		maxslope = 10,
		-- combat
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "MEDIUM_UNIT",
		-- properties
		maxdamage = 200,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		-- other abilities
		cansubmerge = 1,
		canloopbackattack = 1,
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
		moverate1 = 8,
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
				"seapsel1",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
		weapons = {
			{
				name = "ARM_SEAPLANE_FIGHTER_MISSILE",
			},
			{
				name = "ARM_SEAPLANE_FIGHTER_MISSILE",
			},
		},
	},
}
