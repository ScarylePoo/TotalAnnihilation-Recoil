-- ARM_T1_VEH_Podger (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_veh_podger = {
		-- id
		name = "Podger",
		description = "Mine Layer Vehicle",
		side = "ARM",
		unitname = "arm_t1_veh_podger",
		buildoptions = Shared.buildListArmMineLayer,
		objectname = "ARM_T1_VEH_Podger.s3o",
		buildpic = "ARM_T1_VEH_Podger.png",
		script = "ARM_T1_VEH_Podger.lua",
		corpse = "ARM_T1_VEH_Podger_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL1 NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1031,
		buildcostmetal = 173,
		buildtime = 1519,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 0,
		canguard = 0,
		maxvelocity = 0.9,  -- TA 3.1c (was 1.1)
		brakerate = 0.08,
		acceleration = 0.015,
		turnrate = 250,
		maxwaterdepth = 0,
		maxslope = 16,
		-- nanolathing
		builder = 1,
		workertime = 100,  -- TA 3.1c (was 110)
		builddistance = 70,  -- TA 3.1c (was 128)
		canassist = 0,
		canreclaim = 0,
		canrepair = 0,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1200,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 155,  -- TA 3.1c (was 270)
		-- unit animation
		leavetracks = 1,
		trackwidth = 24,
		trackoffset = 3,
		trackstrength = 5,
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
		sounds = {
			arrived = {
				"varmstop",
			},
			build = "nanlath1",
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
			repair = "repair1",
			select = {
				"varmsel",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
