-- CORE_T1_HOV_Slinger (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_hov_slinger = {
		-- id
		name = "Slinger",
		description = "Anti-Air Hovercraft",
		side = "CORE",
		unitname = "core_t1_hov_slinger",
		objectname = "CORE_T1_HOV_Slinger.s3o",
		corpse = "CORE_T1_HOV_Slinger_dead",
		icontype = "hover",
		category = "CORE HOVER LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1542,
		buildcostmetal = 115,
		buildtime = 3747,
		-- movement or placement
		movementclass = "TANKHOVER3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canhover = 1,
		maxvelocity = 3.1,
		brakerate = 0.09,
		acceleration = 0.06,
		turnrate = 280,
		maxwaterdepth = 0,
		maxslope = 16,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		nochasecategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 395,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 490,
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
				"hovmdof2",
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
				"hovmdok2",
			},
			select = {
				"hovmdsl2",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORAH_WEAPON",
			},
		},
	},
}
