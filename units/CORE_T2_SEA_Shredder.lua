-- CORE_T2_SEA_Shredder (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_sea_shredder = {
		-- id
		name = "Shredder",
		description = "Anti-Air Ship",
		side = "CORE",
		unitname = "core_t2_sea_shredder",
		objectname = "CORE_T2_SEA_Shredder",
		corpse = "CORE_T2_SEA_Shredder_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 17921,
		buildcostmetal = 1314,
		buildtime = 41791,
		-- movement or placement
		movementclass = "SMALL_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.8,
		brakerate = 0.018,
		acceleration = 0.02,
		turnrate = 145,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		nochasecategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 2450,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		buildangle = 16384,
		sounds = {
			arrived = {
				"sharmstp",
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
				"sharmmov",
			},
			select = {
				"sharmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORE_ANTI-AIR_SHIP_MISSILE",
			},
			{
				name = "CORE_ANTI-AIR_SHIP_MISSILE",
			},
			{
				name = "CORARCH_WEAPON3",
			},
		},
	},
}
