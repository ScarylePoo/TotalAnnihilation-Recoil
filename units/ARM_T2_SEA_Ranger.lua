-- ARM_T2_SEA_Ranger (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_sea_ranger = {
		-- id
		name = "Ranger",
		description = "Missile Ship",
		side = "ARM",
		unitname = "arm_t2_sea_ranger",
		objectname = "ARM_T2_SEA_Ranger.s3o",
		buildpic = "ARM_T2_SEA_Ranger.png",
		script = "ARM_T2_SEA_Ranger.lua",
		corpse = "ARM_T2_SEA_Ranger_dead",
		category = "ARM SHIP LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7804,
		buildcostmetal = 2348,
		buildtime = 22317,
		-- movement or placement
		movementclass = "MEDIUM_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 1,  -- TA 3.1c (was 1.5)
		brakerate = 0.022,  -- TA 3.1c (was 0.032)
		acceleration = 0.01,  -- TA 3.1c (was 0.02)
		turnrate = 134,  -- TA 3.1c (was 268)
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1200,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 245,  -- TA 3.1c (was 428)
		-- unit animation
		footprintx = 6,
		footprintz = 6,
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
				name = "ARM_SHIP_ROCKET",
				onlytargetcategory = "NOTAIR",
			},
			{
				name = "ARMSHIP_MISSILE",
			},
		},
	},
}
