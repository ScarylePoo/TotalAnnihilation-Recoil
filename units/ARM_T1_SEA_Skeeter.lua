-- ARM_T1_SEA_Skeeter (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_sea_skeeter = {
		-- id
		name = "Skeeter",
		description = "Scout Ship",
		side = "ARM",
		unitname = "arm_t1_sea_skeeter",
		objectname = "ARM_T1_SEA_Skeeter.s3o",
		buildpic = "ARM_T1_SEA_Skeeter.png",
		script = "ARM_T1_SEA_Skeeter.lua",
		corpse = "ARM_T1_SEA_Skeeter_dead",
		category = "ARM SHIP LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 985,
		buildcostmetal = 100,
		buildtime = 2062,  -- TA 3.1c (was 2000)
		-- movement or placement
		movementclass = "SMALL_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 3.8,
		brakerate = 0.02,
		acceleration = 0.1,
		turnrate = 511,
		-- combat
		firestate = 2,
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 560,  -- TA 3.1c (was 360)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 280,  -- TA 3.1c (was 490)
		-- unit animation
		waterline = 2,
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
				name = "ARMPT_LASER",
			},
			{
				name = "ARMKBOT_MISSILE",
				onlytargetcategory = "VTOL",
			},
		},
	},
}
