-- CORE_T1_HOV_Turtle (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_hov_turtle = {
		-- id
		name = "Turtle",
		description = "Transport Hovercraft",
		side = "CORE",
		unitname = "core_t1_hov_turtle",
		objectname = "CORE_T1_HOV_Turtle.s3o",
		corpse = "CORE_T1_HOV_Turtle_dead",
		icontype = "hover",
		category = "CORE HOVER LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7541,
		buildcostmetal = 650,
		buildtime = 19587,
		-- movement or placement
		movementclass = "TANKHOVER3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canhover = 1,
		maxvelocity = 2.3,
		brakerate = 0.017,
		acceleration = 0.03,
		turnrate = 128,
		minwaterdepth = 12,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1080,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 438,
		-- other abilities
		canload = 1,
		transportsize = 6,
		transportcapacity = 5,
		transportmaxunits = 6,
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
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		buildangle = 16384,
		sounds = {
			arrived = {
				"hovlgof2",
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
				"hovlgok2",
			},
			select = {
				"hovlgsl2",
			},
			underattack = "warning1",
		},
	},
}
