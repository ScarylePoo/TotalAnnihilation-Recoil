-- CORE_T1_SEAPL_Voodoo (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seapl_voodoo = {
		-- id
		name = "Voodoo",
		description = "Seaplane Fighter",
		side = "CORE",
		unitname = "core_t1_seapl_voodoo",
		objectname = "CORE_T1_SEAPL_Voodoo",
		corpse = "CORE_T1_SEAPL_Voodoo_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL1 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 6524,
		buildcostmetal = 282,
		buildtime = 14857,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 100,  -- 70
		maxvelocity = 14.1,
		brakerate = 4.5,
		acceleration = 0.48,
		turnrate = 712,
		maxwaterdepth = 255,
		maxslope = 10,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "MEDIUM_UNIT",
		-- properties
		maxdamage = 200,
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
		amphibious = 1,
		canloopbackattack = 1,
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
				name = "CORE_SEAPLANE_FIGHTER_MISSILE",
			},
			{
				name = "CORE_SEAPLANE_FIGHTER_MISSILE",
			},
		},
	},
}
