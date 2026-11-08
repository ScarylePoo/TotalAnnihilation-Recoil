-- ARM_T2_BOT_Marky (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_marky = {
		-- id
		name = "Marky",
		description = "Mobile Radar Kbot",
		side = "ARM",
		unitname = "arm_t2_bot_marky",
		objectname = "ARM_T2_BOT_Marky.s3o",
		buildpic = "ARM_T2_BOT_Marky.png",
		script = "ARM_T2_BOT_Marky.lua",
		corpse = "ARM_T2_BOT_Marky_dead",
		category = "ARM KBOT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1152,
		buildcostmetal = 95,
		buildtime = 3800,
		energyuse = 15,
		energymake = 15,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 0.94,  -- TA 3.1c (was 1.3)
		brakerate = 0.018,
		acceleration = 0.045,
		turnrate = 505,
		maxwaterdepth = 0,
		maxslope = 16,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 320,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 240,  -- TA 3.1c (was 420)
		radardistance = 1250,  -- TA 3.1c (was 1850)
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
		footprintx = 2,
		footprintz = 2,
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
				"kbarmstp",
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
				"kbarmmov",
			},
			select = {
				"kbarmsel",
			},
			underattack = "warning1",
		},
	},
}
