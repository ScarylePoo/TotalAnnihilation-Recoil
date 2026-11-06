-- CORE_T1_SEA_Enforcer (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_sea_enforcer = {
		-- id
		name = "Enforcer",
		description = "Destroyer",
		side = "CORE",
		unitname = "core_t1_sea_enforcer",
		objectname = "CORE_T1_SEA_Enforcer.s3o",
		buildpic = "CORE_T1_SEA_Enforcer.png",
		script = "CORE_T1_SEA_Enforcer.lua",
		corpse = "CORE_T1_SEA_Enforcer_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4505,  -- TA 3.1c (was 4805)
		buildcostmetal = 887,  -- TA 3.1c (was 890)
		buildtime = 13368,  -- TA 3.1c (was 10368)
		-- movement or placement
		movementclass = "SMALL_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.93,
		brakerate = 0.0183,  -- TA 3.1c (was 0.02)
		acceleration = 0.0092,  -- TA 3.1c (was 0.05)
		turnrate = 128,  -- TA 3.1c (was 256)
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 3150,  -- TA 3.1c (was 1950)
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 330,  -- TA 3.1c (was 577)
		sonardistance = 305,  -- TA 3.1c (was 455)
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		waterline = 1,
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
				name = "CORE_ROY",
			},
			{
				name = "CORE_DEPTHCHARGE",
			},
		},
	},
}
