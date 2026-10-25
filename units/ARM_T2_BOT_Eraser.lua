-- ARM_T2_BOT_Eraser (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_eraser = {
		-- id
		name = "Eraser",
		description = "Radar Jammer",
		side = "ARM",
		unitname = "arm_t2_bot_eraser",
		objectname = "ARM_T2_BOT_Eraser",
		corpse = "ARM_T2_BOT_Eraser_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1326,
		buildcostmetal = 73,
		buildtime = 4937,
		energyuse = 10,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.3,
		brakerate = 1,
		acceleration = 0.17,
		turnrate = 950,
		maxwaterdepth = 112,
		maxslope = 32,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 305,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 350,
		radardistancejam = 600,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 22,
		trackoffset = 0,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "KbotTrack",
		footprintx = 1,
		footprintz = 1,
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
			activate = "radjam1",
			arrived = {
				"varmstop",
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
			deactivate = "radjam1",
			ok = {
				"varmmove",
			},
			select = {
				"radjam1",
			},
			underattack = "warning1",
		},
	},
}
