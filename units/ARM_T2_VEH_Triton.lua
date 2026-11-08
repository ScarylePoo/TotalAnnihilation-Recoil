-- ARM_T2_VEH_Triton (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_triton = {
		-- id
		name = "Triton",
		description = "Amphibious Tank",
		side = "ARM",
		unitname = "arm_t2_veh_triton",
		objectname = "ARM_T2_VEH_Triton.s3o",
		buildpic = "ARM_T2_VEH_Triton.png",
		script = "ARM_T2_VEH_Triton.lua",
		corpse = "ARM_T2_VEH_Triton_dead",
		category = "ARM TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2300,  -- TA 3.1c (was 2900)
		buildcostmetal = 298,  -- TA 3.1c (was 345)
		buildtime = 6112,
		-- movement or placement
		movementclass = "AMPHTANK",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.3,
		brakerate = 0.008,
		acceleration = 0.009,  -- TA 3.1c (was 0.017)
		turnrate = 350,  -- TA 3.1c (was 370)
		maxwaterdepth = 255,
		maxslope = 12,
		-- combat
		firestate = -1,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1230,  -- TA 3.1c (was 2230)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 240,  -- TA 3.1c (was 420)
		-- unit animation
		leavetracks = 1,
		trackwidth = 40,
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
				name = "ARM_MEDIUMCANNON",
			},
		},
	},
}
