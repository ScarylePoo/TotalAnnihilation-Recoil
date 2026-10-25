-- ARM_T1_HOV_Bear (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_hov_bear = {
		-- id
		name = "Bear",
		description = "Transport Hovercraft",
		side = "ARM",
		unitname = "arm_t1_hov_bear",
		objectname = "ARM_T1_HOV_Bear",
		corpse = "ARM_T1_HOV_Bear_dead",
		icontype = "hover",
		category = "ARM HOVER LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7938,
		buildcostmetal = 665,
		buildtime = 20341,
		-- movement or placement
		movementclass = "TANKHOVER3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canhover = 1,
		maxvelocity = 2,
		brakerate = 0.018,
		acceleration = 0.04,
		turnrate = 128,
		minwaterdepth = 12,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1150,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 437,
		-- other abilities
		canload = 1,
		transportmaxunits = 6,
		transportsize = 6,
		transportcapacity = 5,
		-- unit animation
		waterline = 4,
		footprintx = 4,
		footprintz = 4,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		scale = 0.5,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		buildangle = 16384,
		sounds = {
			arrived = {
				"hovlgof1",
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
				"hovlgok1",
			},
			select = {
				"hovlgsl1",
			},
			underattack = "warning1",
		},
	},
}
