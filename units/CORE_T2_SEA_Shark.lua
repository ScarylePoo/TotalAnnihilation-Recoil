-- CORE_T2_SEA_Shark (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_sea_shark = {
		-- id
		name = "Shark",
		description = "Submarine Killer",
		side = "CORE",
		unitname = "core_t2_sea_shark",
		objectname = "CORE_T2_SEA_Shark",
		corpse = "CORE_T2_SEA_Shark_dead",
		icontype = "ship",
		category = "CORE UNDERWATER LEVEL2 WEAPON NOTAIR",
		-- costs, makes, uses, storage
		buildcostenergy = 5245,
		buildcostmetal = 1356,
		buildtime = 17529,
		-- movement or placement
		movementclass = "SHIP_SUBMARINE",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.5,
		brakerate = 0.2,
		acceleration = 0.03,
		turnrate = 303,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 376,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 262,
		sonardistance = 700,
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
				name = "CORSMART_TORPEDO",
			},
		},
	},
}
