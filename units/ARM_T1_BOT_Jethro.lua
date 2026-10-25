-- ARM_T1_BOT_Jethro (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_bot_jethro = {
		-- id
		name = "Jethro",
		description = "Anti-Air Kbot",
		side = "ARM",
		unitname = "arm_t1_bot_jethro",
		objectname = "ARM_T1_BOT_Jethro",
		corpse = "ARM_T1_BOT_Jethro_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1219,
		buildcostmetal = 128,
		buildtime = 2631,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.6,
		brakerate = 0.15,
		acceleration = 0.1,
		turnrate = 1016,
		-- combat
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 470,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 375,
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
				name = "ARMKBOT_MISSILE",
			},
		},
	},
}
