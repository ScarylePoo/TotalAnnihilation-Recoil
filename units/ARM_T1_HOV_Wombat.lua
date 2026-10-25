-- ARM_T1_HOV_Wombat (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_hov_wombat = {
		-- id
		name = "Wombat",
		description = "Hovercraft Rocket Launcher",
		side = "ARM",
		unitname = "arm_t1_hov_wombat",
		objectname = "ARM_T1_HOV_Wombat",
		corpse = "ARM_T1_HOV_Wombat_dead",
		icontype = "hover",
		category = "ARM HOVER LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3131,
		buildcostmetal = 325,
		buildtime = 17933,
		-- movement or placement
		movementclass = "TANKHOVER3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canhover = 1,
		maxvelocity = 2.3,
		brakerate = 0.09,
		acceleration = 0.03,
		turnrate = 240,
		maxwaterdepth = 0,
		maxslope = 16,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 450,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 280,
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
				name = "ARM_HOVER_ROCKET",
				onlytargetcategory = "NOTAIR",
			},
		},
	},
}
