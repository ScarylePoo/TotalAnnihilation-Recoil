-- CORE_T1_BOT_Crasher (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_bot_crasher = {
		-- id
		name = "Crasher",
		description = "Missile Kbot",
		side = "CORE",
		unitname = "core_t1_bot_crasher",
		objectname = "CORE_T1_BOT_Crasher.s3o",
		buildpic = "CORE_T1_BOT_Crasher.png",
		script = "CORE_T1_BOT_Crasher.lua",          -- walker: Lua script on the standard skeleton (was the COB)
		-- Script=CORE_T1_BOT_Crasher.lua;
		corpse = "CORE_T1_BOT_Crasher_dead",
		category = "CORE KBOT LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1224,
		buildcostmetal = 129,
		buildtime = 2636,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.25,  -- TA 3.1c (was 1.5)
		brakerate = 0.15,
		acceleration = 0.1,
		turnrate = 1011,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 480,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 292,  -- TA 3.1c (was 355)
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
				"kbcorstp",
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
				"kbcormov",
			},
			select = {
				"kbcorsel",
			},
			underattack = "warning1",
		},
		weapons = {
			[3] = {
				name = "CORKBOT_MISSILE",
			},
		},
	},
}
