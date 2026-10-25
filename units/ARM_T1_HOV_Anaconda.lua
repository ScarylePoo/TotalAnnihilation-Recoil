-- ARM_T1_HOV_Anaconda (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_hov_anaconda = {
		-- id
		name = "Anaconda",
		description = "Hovertank",
		side = "ARM",
		unitname = "arm_t1_hov_anaconda",
		objectname = "ARM_T1_HOV_Anaconda",
		corpse = "ARM_T1_HOV_Anaconda_dead",
		icontype = "hover",
		category = "ARM HOVER LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2856,
		buildcostmetal = 272,
		buildtime = 8115,
		-- movement or placement
		movementclass = "TANKHOVER3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canhover = 1,
		maxvelocity = 2.8,
		brakerate = 0.11,
		acceleration = 0.09,
		turnrate = 250,
		maxwaterdepth = 0,
		maxslope = 16,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1280,
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
				"hovmdof1",
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
				"hovmdok1",
			},
			select = {
				"hovmdsl1",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARMANAC_WEAPON",
			},
		},
	},
}
