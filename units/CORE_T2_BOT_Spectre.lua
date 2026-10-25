-- CORE_T2_BOT_Spectre (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_spectre = {
		-- id
		name = "Spectre",
		description = "Radar Jammer",
		side = "CORE",
		unitname = "core_t2_bot_spectre",
		objectname = "CORE_T2_BOT_Spectre",
		corpse = "CORE_T2_BOT_Spectre_dead",
		icontype = "kbot",
		category = "CORE KBOT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1453,
		buildcostmetal = 70,
		buildtime = 5439,
		energyuse = 10,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.3,
		brakerate = 0.12,
		acceleration = 0.1,
		turnrate = 945,
		maxwaterdepth = 112,
		maxslope = 32,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 310,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 200,
		radardistancejam = 590,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		upright = 1,
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
			activate = "radjam2",
			arrived = {
				"vcorstop",
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
			deactivate = "radjam2",
			ok = {
				"vcormove",
			},
			select = {
				"radjam2",
			},
			underattack = "warning1",
		},
	},
}
