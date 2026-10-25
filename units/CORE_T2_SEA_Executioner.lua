-- CORE_T2_SEA_Executioner (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_sea_executioner = {
		-- id
		name = "Executioner",
		description = "Cruiser",
		side = "CORE",
		unitname = "core_t2_sea_executioner",
		objectname = "CORE_T2_SEA_Executioner",
		corpse = "CORE_T2_SEA_Executioner_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 10689,
		buildcostmetal = 2155,
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
		acceleration = 0.025,
		turnrate = 256,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 4370,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 600,
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
