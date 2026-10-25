-- CORE_T1_SEAPL_Typhoon (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seapl_typhoon = {
		-- id
		name = "Typhoon",
		description = "Torpedo Seaplane",
		side = "CORE",
		unitname = "core_t1_seapl_typhoon",
		objectname = "CORE_T1_SEAPL_Typhoon",
		corpse = "CORE_T1_SEAPL_Typhoon_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL1 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7785,
		buildcostmetal = 365,
		buildtime = 23698,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 100,
		maxvelocity = 10.5,
		brakerate = 4,
		acceleration = 0.36,
		turnrate = 512,
		maxwaterdepth = 255,
		maxslope = 10,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "MEDIUM_UNIT",
		-- properties
		maxdamage = 310,
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
		attackrunlength = 100,
		amphibious = 1,
		cansubmerge = 1,
		sounds = {
			arrived = {
				"vtolcrld",
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
				"seapsel2",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
		weapons = {
			{
				badtargetcategory = "VTOL",
				name = "CORSEAP_WEAPON1",
			},
			{
				name = "CORSEAP_WEAPON2",
			},
			{
				name = "CORSEAP_WEAPON3",
			},
		},
	},
}
