-- CORE_T1_BOT_Ak (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_bot_ak = {
		-- id
		name = "A.K.",
		description = "Infantry Kbot",
		side = "CORE",
		unitname = "core_t1_bot_ak",
		objectname = "CORE_T1_BOT_Ak.s3o",
		script = "CORE_T1_BOT_Ak.lua",          -- walker: Lua script on the standard skeleton (was the COB)
		corpse = "CORE_T1_BOT_Ak_dead",
		icontype = "kbot",
		category = "CORE KBOT LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 696,
		buildcostmetal = 62,
		buildtime = 1523,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.2,
		brakerate = 0.18,
		acceleration = 0.09,
		turnrate = 1100,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 339,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 481,
		-- unit animation
		upright = 1,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 22,
		trackoffset = 0,
		trackstrength = 5,
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
				"servtny1",
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
				"servtny1",
			},
			select = {
				"servtny1",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORE_LASER",
			},
		},
	},
}
