-- ARM_T1_VEH_Stumpy (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_veh_stumpy = {
		-- id
		name = "Stumpy",
		description = "Medium Assault Tank",
		side = "ARM",
		unitname = "arm_t1_veh_stumpy",
		objectname = "ARM_T1_VEH_Stumpy.s3o",
		buildpic = "ARM_T1_VEH_Stumpy.png",
		script = "ARM_T1_VEH_Stumpy.lua",
		corpse = "ARM_T1_VEH_Stumpy_dead",
		category = "ARM TANK LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1246,
		buildcostmetal = 165,
		buildtime = 2404,
		-- movement or placement
		movementclass = "TANKSH2",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.7,  -- TA 3.1c (was 2.1)
		brakerate = 0.01,  -- TA 3.1c (was 0.025)
		acceleration = 0.016,  -- TA 3.1c (was 0.058)
		turnrate = 450,  -- TA 3.1c (was 550)
		maxwaterdepth = 12,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 992,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 250,  -- TA 3.1c (was 438)
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
				"tarmst0p",
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
				"tarmmove",
			},
			select = {
				"tarmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_LIGHTCANNON",
			},
		},
	},
}
