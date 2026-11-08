-- ARM_T2_VEH_Seer (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_seer = {
		-- id
		name = "Seer",
		description = "Mobile Radar",
		side = "ARM",
		unitname = "arm_t2_veh_seer",
		objectname = "ARM_T2_VEH_Seer.s3o",
		buildpic = "ARM_T2_VEH_Seer.png",
		script = "ARM_T2_VEH_Seer.lua",
		corpse = "ARM_T2_VEH_Seer_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 941,
		buildcostmetal = 85,
		buildtime = 3186,
		energyuse = 8,
		energymake = 8,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.1,  -- TA 3.1c (was 1.3)
		brakerate = 0.012,  -- TA 3.1c (was 0.02)
		acceleration = 0.032,  -- TA 3.1c (was 0.035)
		turnrate = 500,
		maxwaterdepth = 0,
		maxslope = 16,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 480,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 320,  -- TA 3.1c (was 560)
		radardistance = 1120,  -- TA 3.1c (was 1720)
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		leavetracks = 1,
		trackwidth = 20,
		trackoffset = 8,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "VehTrack",
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
				"varmstop",
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
				"varmmove",
			},
			select = {
				"varmsel",
			},
			underattack = "warning1",
		},
	},
}
