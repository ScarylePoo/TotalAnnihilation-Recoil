-- CORE_T1_SEA_Searcher (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_sea_searcher = {
		-- id
		name = "Searcher",
		description = "Scout Ship",
		side = "CORE",
		unitname = "core_t1_sea_searcher",
		objectname = "CORE_T1_SEA_Searcher",
		corpse = "CORE_T1_SEA_Searcher_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 917,
		buildcostmetal = 95,
		buildtime = 1877,
		-- movement or placement
		movementclass = "SMALL_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 3.6,
		brakerate = 0.02,
		acceleration = 0.1,
		turnrate = 519,
		-- combat
		firestate = 2,
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 470,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 490,
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
		maneuverleashlength = 1280,
		ovradjust = 1,
		sounds = {
			arrived = {
				"shcorstp",
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
				"shcormov",
			},
			select = {
				"shcorsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORE_SCOUT_LASER",
			},
			{
				name = "CORKBOT_MISSILE",
				onlytargetcategory = "VTOL",
			},
		},
	},
}
