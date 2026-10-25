-- ARM_T1_SEAPL_Albatross (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seapl_albatross = {
		-- id
		name = "Albatross",
		description = "Torpedo Seaplane",
		side = "ARM",
		unitname = "arm_t1_seapl_albatross",
		objectname = "ARM_T1_SEAPL_Albatross",
		corpse = "ARM_T1_SEAPL_Albatross_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL1 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 9619,
		buildcostmetal = 257,
		buildtime = 22825,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 100,
		maxvelocity = 10.4,
		brakerate = 4,
		acceleration = 0.37,
		turnrate = 452,
		maxwaterdepth = 255,
		maxslope = 10,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "MEDIUM_UNIT",
		-- properties
		maxdamage = 316,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		-- other abilities
		cansubmerge = 1,
		-- unit animation
		collide = 0,
		footprintx = 3,
		footprintz = 3,
		-- what are these? or more importantly, do they work/have meaning?
		amphibious = 1,
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		bankscale = 1,
		defaultmissiontype = "VTOL_standby",
		maneuverleashlength = 1280,
		moverate1 = 8,
		attackrunlength = 100,
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
				badtargetcategory = "VTOL",
				name = "ARMSEAP_WEAPON1",
			},
			{
				name = "ARMSEAP_WEAPON2",
			},
			{
				name = "ARMSEAP_WEAPON3",
			},
		},
	},
}
