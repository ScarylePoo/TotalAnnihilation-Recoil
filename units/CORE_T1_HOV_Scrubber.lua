-- CORE_T1_HOV_Scrubber (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_hov_scrubber = {
		-- id
		name = "Scrubber",
		description = "Scout Hovercraft",
		side = "CORE",
		unitname = "core_t1_hov_scrubber",
		objectname = "CORE_T1_HOV_Scrubber.s3o",
		buildpic = "CORE_T1_HOV_Scrubber.png",
		script = "CORE_T1_HOV_Scrubber.lua",
		corpse = "CORE_T1_HOV_Scrubber_dead",
		icontype = "hover",
		category = "CORE HOVER LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1252,
		buildcostmetal = 72,
		buildtime = 3547,
		-- movement or placement
		movementclass = "TANKHOVER3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canhover = 1,
		maxvelocity = 3.5,  -- TA 3.1c (was 3.7)
		brakerate = 0.05,
		acceleration = 0.1,
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
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 280,  -- TA 3.1c (was 560)
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
				"hovsmok2",
			},
			select = {
				"hovsmsl2",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORSH_WEAPON",
			},
		},
	},
}
