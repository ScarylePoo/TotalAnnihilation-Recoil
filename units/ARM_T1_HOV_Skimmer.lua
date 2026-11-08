-- ARM_T1_HOV_Skimmer (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_hov_skimmer = {
		-- id
		name = "Skimmer",
		description = "Scout Hovercraft",
		side = "ARM",
		unitname = "arm_t1_hov_skimmer",
		objectname = "ARM_T1_HOV_Skimmer.s3o",
		buildpic = "ARM_T1_HOV_Skimmer.png",
		script = "ARM_T1_HOV_Skimmer.lua",
		corpse = "ARM_T1_HOV_Skimmer_dead",
		category = "ARM HOVER LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1169,
		buildcostmetal = 76,
		buildtime = 3388,
		-- movement or placement
		movementclass = "TANKHOVER3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canhover = 1,
		maxvelocity = 3.7,
		brakerate = 0.05,
		acceleration = 0.11,  -- TA 3.1c (was 0.18)
		turnrate = 310,
		maxwaterdepth = 0,
		maxslope = 16,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 200,  -- TA 3.1c (was 240)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 280,  -- TA 3.1c (was 580)
		-- unit animation
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
				"hovsmof2",
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
				"hovsmok1",
			},
			select = {
				"hovsmsl1",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARMSH_WEAPON",
			},
		},
	},
}
