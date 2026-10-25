-- ARM_T1_BOT_Flea (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_bot_flea = {
		-- id
		name = "Flea",
		description = "Fast Light Scout Kbot",
		side = "ARM",
		unitname = "arm_t1_bot_flea",
		objectname = "ARM_T1_BOT_Flea.s3o",
		script = "ARM_T1_BOT_Flea.lua",          -- walker: Lua script on the standard skeleton (was the COB)
		corpse = "ARM_T1_BOT_Flea_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 218,
		buildcostmetal = 24,
		buildtime = 1013,
		-- movement or placement
		movementclass = "KBOTGOOD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 3.5,
		brakerate = 0.25,
		acceleration = 0.14,
		turnrate = 1300,
		maxwaterdepth = 0,
		maxslope = 32,
		-- combat
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 75,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 460,
		radardistance = 700,
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		upright = 1,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 10,
		trackoffset = 0,
		trackstrength = 7,
		trackstretch = 1,
		tracktype = "KbotTrack",
		footprintx = 2,
		footprintz = 2,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 2,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		ovradjust = 1,
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
		weapons = {
			{
				name = "ARM_FLEA_LASER",
			},
		},
	},
}
