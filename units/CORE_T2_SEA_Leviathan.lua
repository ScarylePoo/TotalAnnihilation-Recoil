-- CORE_T2_SEA_Leviathan (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_sea_leviathan = {
		-- id
		name = "Leviathan",
		description = "Battle Sub",
		side = "CORE",
		unitname = "core_t2_sea_leviathan",
		objectname = "CORE_T2_SEA_Leviathan",
		corpse = "CORE_T2_SEA_Leviathan_dead",
		icontype = "ship",
		category = "CORE UNDERWATER LEVEL2 WEAPON NOTAIR",
		-- costs, makes, uses, storage
		buildcostenergy = 19940,
		buildcostmetal = 3850,
		buildtime = 38567,
		-- movement or placement
		movementclass = "SHIP_SUBMARINE",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.5,
		brakerate = 0.016,
		acceleration = 0.03,
		turnrate = 196,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 3052,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 650,
		sonardistance = 1130,
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
				name = "CORSSUB_WEAPON",
			},
		},
	},
}
