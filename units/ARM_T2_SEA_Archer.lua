-- ARM_T2_SEA_Archer (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_sea_archer = {
		-- id
		name = "Archer",
		description = "Anti-Air Ship",
		side = "ARM",
		unitname = "arm_t2_sea_archer",
		objectname = "ARM_T2_SEA_Archer",
		corpse = "ARM_T2_SEA_Archer_dead",
		icontype = "ship",
		category = "ARM SHIP LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 17058,
		buildcostmetal = 1358,
		buildtime = 38628,
		-- movement or placement
		movementclass = "SMALL_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 3,
		brakerate = 0.018,
		acceleration = 0.02,
		turnrate = 160,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		nochasecategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 2360,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
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
		buildangle = 16384,
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
		weapons = {
			{
				name = "ARM_ANTI-AIR_SHIP_MISSILE",
			},
			{
				name = "ARM_ANTI-AIR_SHIP_MISSILE",
			},
			{
				name = "ARMAAS_WEAPON3",
				onlytargetcategory = "VTOL",
			},
		},
	},
}
