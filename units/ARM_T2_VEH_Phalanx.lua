-- ARM_T2_VEH_Phalanx (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_phalanx = {
		-- id
		name = "Phalanx",
		description = "Mobile Flak Vehicle",
		side = "ARM",
		unitname = "arm_t2_veh_phalanx",
		objectname = "ARM_T2_VEH_Phalanx.s3o",
		buildpic = "ARM_T2_VEH_Phalanx.png",
		script = "ARM_T2_VEH_Phalanx.lua",
		corpse = "ARM_T2_VEH_Phalanx_dead",
		category = "ARM TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 10500,
		buildcostmetal = 830,
		buildtime = 20380,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.21,  -- TA 3.1c (was 1.43)
		brakerate = 0.012,
		acceleration = 0.03,
		turnrate = 511,
		maxwaterdepth = 12,
		maxslope = 16,
		-- combat
		firestate = 2,
		nochasecategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 621,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 300,  -- TA 3.1c (was 525)
		-- unit animation
		leavetracks = 1,
		trackwidth = 27,
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
		maneuverleashlength = 10,
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
				name = "ARMyork_GUN",
				onlytargetcategory = "VTOL",
			},
		},
	},
}
