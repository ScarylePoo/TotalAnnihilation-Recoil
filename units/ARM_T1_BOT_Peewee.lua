-- ARM_T1_BOT_Peewee (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_bot_peewee = {
		-- id
		name = "Peewee",
		description = "Infantry Kbot",
		side = "ARM",
		unitname = "arm_t1_bot_peewee",
		objectname = "ARM_T1_BOT_Peewee",
		corpse = "ARM_T1_BOT_Peewee_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 697,
		buildcostmetal = 67,
		buildtime = 1452,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.5,
		brakerate = 0.19,
		acceleration = 0.1,
		turnrate = 1120,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 325,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 490,
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
				"servtny2",
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
				"servtny2",
			},
			select = {
				"servtny2",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "EMG",
			},
		},
	},
}
