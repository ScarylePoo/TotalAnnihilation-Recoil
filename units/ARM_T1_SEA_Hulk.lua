-- ARM_T1_SEA_Hulk (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_sea_hulk = {
		-- id
		name = "Hulk",
		description = "Transport Ship",
		side = "ARM",
		unitname = "arm_t1_sea_hulk",
		objectname = "ARM_T1_SEA_Hulk",
		corpse = "ARM_T1_SEA_Hulk_dead",
		icontype = "ship",
		category = "ARM SHIP LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 6639,
		buildcostmetal = 1293,
		buildtime = 14538,
		-- movement or placement
		movementclass = "MEDIUM_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 1.9,
		brakerate = 0.018,
		acceleration = 0.019,
		turnrate = 256,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 4000,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 437,
		-- other abilities
		canload = 1,
		transportsize = 20,
		transportcapacity = 20,
		transportmass = 28000,  -- core krog mass is 29800
		-- unit animation
		waterline = 15,
		footprintx = 6,
		footprintz = 6,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		scale = 0.5,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		buildangle = 16384,
		ovradjust = 1,
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
