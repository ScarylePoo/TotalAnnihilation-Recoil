-- CORE_T1_SEA_Snake (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_sea_snake = {
		-- id
		name = "Snake",
		description = "Submarine",
		side = "CORE",
		unitname = "core_t1_sea_snake",
		objectname = "CORE_T1_SEA_Snake.s3o",
		corpse = "CORE_T1_SEA_Snake_dead",
		icontype = "ship",
		category = "CORE UNDERWATER LEVEL1 WEAPON NOTAIR",
		-- costs, makes, uses, storage
		buildcostenergy = 3902,
		buildcostmetal = 1199,
		buildtime = 9729,
		-- movement or placement
		movementclass = "SHIP_SUBMARINE",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1,
		brakerate = 0.2,
		acceleration = 0.03,
		turnrate = 256,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 590,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 196,
		sonardistance = 700,
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		waterline = 30,
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
				"sucorstp",
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
				"sucormov",
			},
			select = {
				"sucorsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORE_TORPEDO",
			},
		},
	},
}
