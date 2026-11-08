-- CORE_T1_SEA_Envoy (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_sea_envoy = {
		-- id
		name = "Envoy",
		description = "Transport Ship",
		side = "CORE",
		unitname = "core_t1_sea_envoy",
		objectname = "CORE_T1_SEA_Envoy.s3o",
		buildpic = "CORE_T1_SEA_Envoy.png",
		script = "CORE_T1_SEA_Envoy.lua",
		corpse = "CORE_T1_SEA_Envoy_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4786,  -- TA 3.1c (was 6786)
		buildcostmetal = 887,  -- TA 3.1c (was 1187)
		buildtime = 13663,
		-- movement or placement
		movementclass = "MEDIUM_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 1.8,
		brakerate = 0.0183,  -- TA 3.1c (was 0.02)
		acceleration = 0.0092,  -- TA 3.1c (was 0.01)
		turnrate = 130,  -- TA 3.1c (was 260)
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 2120,  -- TA 3.1c (was 4120)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 250,
		-- other abilities
		canload = 1,
		transportsize = 3,  -- TA 3.1c (was 24)
		transportcapacity = 5,  -- TA 3.1c (was 24)
		transportmaxunits = 24,
		transportmass = 28000,  -- so you can't transport a krog
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
	},
}
