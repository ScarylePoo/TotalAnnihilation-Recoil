-- CORE_T2_SEA_Executioner (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_sea_executioner = {
		-- id
		name = "Executioner",
		description = "Cruiser",
		side = "CORE",
		unitname = "core_t2_sea_executioner",
		objectname = "CORE_T2_SEA_Executioner.s3o",
		buildpic = "CORE_T2_SEA_Executioner.png",
		script = "CORE_T2_SEA_Executioner.lua",
		corpse = "CORE_T2_SEA_Executioner_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 8551,  -- TA 3.1c (was 10689)
		buildcostmetal = 1724,  -- TA 3.1c (was 2155)
		buildtime = 17050,
		-- movement or placement
		movementclass = "MEDIUM_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.4,
		brakerate = 0.05,
		acceleration = 0.01,  -- TA 3.1c (was 0.025)
		turnrate = 128,  -- TA 3.1c (was 256)
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 4170,  -- TA 3.1c (was 4370)
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 210,  -- TA 3.1c (was 600)
		sonardistance = 420,
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		footprintx = 6,
		footprintz = 6,
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
				name = "COR_CRUS",
			},
			{
				name = "CORE_DEPTHCHARGE",
			},
		},
	},
}
