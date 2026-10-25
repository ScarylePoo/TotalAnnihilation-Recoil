-- CORE_T2_SEA_Phantom (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_sea_phantom = {
		-- id
		name = "Phantom",
		description = "Radar Jammer Ship",
		side = "CORE",
		unitname = "core_t2_sea_phantom",
		objectname = "CORE_T2_SEA_Phantom",
		corpse = "CORE_T2_SEA_Phantom_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2254,
		buildcostmetal = 135,
		buildtime = 7025,
		energyuse = 20,
		-- movement or placement
		movementclass = "SMALL_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.5,
		brakerate = 0.018,
		acceleration = 0.08,
		turnrate = 375,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "MEDIUM_UNIT",
		-- properties
		maxdamage = 570,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 540,
		radardistancejam = 730,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
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
