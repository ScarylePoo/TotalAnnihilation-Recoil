-- ARM_T1_SEA_Lurker (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_sea_lurker = {
		-- id
		name = "Lurker",
		description = "Submarine",
		side = "ARM",
		unitname = "arm_t1_sea_lurker",
		objectname = "ARM_T1_SEA_Lurker",
		corpse = "ARM_T1_SEA_Lurker_dead",
		icontype = "ship",
		category = "ARM UNDERWATER LEVEL1 WEAPON NOTAIR",
		-- costs, makes, uses, storage
		buildcostenergy = 3724,
		buildcostmetal = 1151,
		buildtime = 9894,
		-- movement or placement
		movementclass = "SHIP_SUBMARINE",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.3,
		brakerate = 0.18,
		acceleration = 0.015,
		turnrate = 256,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 610,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 196,
		sonardistance = 605,
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		waterline = 40,
		footprintx = 3,
		footprintz = 3,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		ovradjust = 1,
		sounds = {
			arrived = {
				"suarmstp",
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
				"suarmmov",
			},
			select = {
				"suarmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_TORPEDO",
			},
		},
	},
}
