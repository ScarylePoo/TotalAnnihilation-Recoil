-- ARM_T2_VEH_Luger (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_luger = {
		-- id
		name = "Luger",
		description = "Mobile Artillery",
		side = "ARM",
		unitname = "arm_t2_veh_luger",
		objectname = "ARM_T2_VEH_Luger.s3o",
		buildpic = "ARM_T2_VEH_Luger.png",
		script = "ARM_T2_VEH_Luger.lua",
		corpse = "ARM_T2_VEH_Luger_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2140,  -- TA 3.1c (was 2621)
		buildcostmetal = 264,  -- TA 3.1c (was 314)
		buildtime = 4530,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1,  -- TA 3.1c (was 1.3)
		brakerate = 0.01,  -- TA 3.1c (was 0.04)
		acceleration = 0.01,  -- TA 3.1c (was 0.02)
		turnrate = 350,
		maxwaterdepth = 0,
		maxslope = 12,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 525,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 220,  -- TA 3.1c (was 385)
		-- unit animation
		leavetracks = 1,
		trackwidth = 32,
		trackoffset = 0,
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
				name = "ARM_ARTILLERY",
			},
		},
	},
}
