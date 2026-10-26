-- CORE_T1_SEA_Envoy (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_sea_envoy = {
		-- id
		name = "Envoy",
		description = "Transport Ship",
		side = "CORE",
		unitname = "core_t1_sea_envoy",
		objectname = "CORE_T1_SEA_Envoy.s3o",
		corpse = "CORE_T1_SEA_Envoy_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 6786,
		buildcostmetal = 1187,
		buildtime = 13663,
		-- movement or placement
		movementclass = "MEDIUM_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 1.8,
		brakerate = 0.02,
		acceleration = 0.01,
		turnrate = 260,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 4120,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 250,
		-- other abilities
		canload = 1,
		transportsize = 24,
		transportcapacity = 24,
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
