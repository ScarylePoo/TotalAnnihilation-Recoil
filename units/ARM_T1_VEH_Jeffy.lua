-- ARM_T1_VEH_Jeffy (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_veh_jeffy = {
		-- id
		name = "Jeffy",
		description = "Fast Scout Vehicle",
		side = "ARM",
		unitname = "arm_t1_veh_jeffy",
		objectname = "ARM_T1_VEH_Jeffy.s3o",
		buildpic = "ARM_T1_VEH_Jeffy.png",
		script = "ARM_T1_VEH_Jeffy.lua",
		corpse = "ARM_T1_VEH_Jeffy_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 564,
		buildcostmetal = 37,
		buildtime = 1465,
		-- movement or placement
		movementclass = "KBOTBAD",  -- TANKSH2
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 3,  -- TA 3.1c (was 3.4)
		brakerate = 0.06,
		acceleration = 0.04,
		turnrate = 499,
		maxwaterdepth = 12,
		maxslope = 18,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 79,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 310,  -- TA 3.1c (was 543)
		radardistance = 0,  -- TA 3.1c (was 800)
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		leavetracks = 1,
		trackwidth = 24,
		trackoffset = 3,
		trackstrength = 5,
		trackstretch = 1,
		tracktype = "VehTrack",
		footprintx = 2,
		footprintz = 2,
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
		weapons = {
			{
				name = "ARM_LASER",
			},
		},
	},
}
