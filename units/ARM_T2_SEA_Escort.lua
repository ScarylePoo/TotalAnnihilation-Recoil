-- ARM_T2_SEA_Escort (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_sea_escort = {
		-- id
		name = "Escort",
		description = "Radar Jammer Ship",
		side = "ARM",
		unitname = "arm_t2_sea_escort",
		objectname = "ARM_T2_SEA_Escort",
		corpse = "ARM_T2_SEA_Escort_dead",
		icontype = "ship",
		category = "ARM SHIP LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1928,
		buildcostmetal = 131,
		buildtime = 6708,
		energyuse = 18,
		-- movement or placement
		movementclass = "SMALL_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.7,
		brakerate = 0.016,
		acceleration = 0.075,
		turnrate = 400,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "MEDIUM_UNIT",
		-- properties
		maxdamage = 510,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		radardistancejam = 700,
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
	},
}
