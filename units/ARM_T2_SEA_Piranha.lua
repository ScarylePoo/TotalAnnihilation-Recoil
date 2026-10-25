-- ARM_T2_SEA_Piranha (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_sea_piranha = {
		-- id
		name = "Piranha",
		description = "Submarine Killer",
		side = "ARM",
		unitname = "arm_t2_sea_piranha",
		objectname = "ARM_T2_SEA_Piranha",
		corpse = "ARM_T2_SEA_Piranha_dead",
		icontype = "ship",
		category = "ARM UNDERWATER LEVEL2 WEAPON NOTAIR",
		-- costs, makes, uses, storage
		buildcostenergy = 5481,
		buildcostmetal = 1448,
		buildtime = 17767,
		-- movement or placement
		movementclass = "SHIP_SUBMARINE",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.4,
		brakerate = 0.36,
		acceleration = 0.2,
		turnrate = 622,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 390,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 262,
		sonardistance = 800,
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
				name = "ARMSMART_TORPEDO",
			},
		},
	},
}
