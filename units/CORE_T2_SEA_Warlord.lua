-- CORE_T2_SEA_Warlord (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_sea_warlord = {
		-- id
		name = "Warlord",
		description = "Battleship",
		side = "CORE",
		unitname = "core_t2_sea_warlord",
		objectname = "CORE_T2_SEA_Warlord",
		corpse = "CORE_T2_SEA_Warlord_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 24676,
		buildcostmetal = 5226,
		buildtime = 40640,
		-- movement or placement
		movementclass = "BIG_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.15,
		brakerate = 0.018,
		acceleration = 0.0175,
		turnrate = 138,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 7940,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		-- unit animation
		footprintx = 8,
		footprintz = 8,
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
				name = "CORE_BATSLASER",
			},
			{
				name = "COR_BATS",
			},
		},
	},
}
