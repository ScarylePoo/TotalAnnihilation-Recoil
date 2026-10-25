-- ARM_T2_SEA_Colossus (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_sea_colossus = {
		-- id
		name = "Colossus",
		description = "Light Carrier",
		side = "ARM",
		unitname = "arm_t2_sea_colossus",
		objectname = "ARM_T2_SEA_Colossus",
		corpse = "ARM_T2_SEA_Colossus_dead",
		icontype = "ship",
		category = "ARM SHIP LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 11257,
		buildcostmetal = 1372,
		buildtime = 25394,
		energymake = 370,
		-- movement or placement
		movementclass = "BIG_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.3,
		brakerate = 0.02,
		acceleration = 0.02,
		turnrate = 128,
		-- nanolathing
		builder = 1,
		workertime = 800,
		canassist = 0,
		canreclaim = 0,
		-- combat
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "ATOMIC_BLAST",
		-- properties
		maxdamage = 3390,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		radardistance = 2500,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		isairbase = 1,
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
