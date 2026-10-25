-- ARM_T1_BOT_Warrior (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_bot_warrior = {
		-- id
		name = "Warrior",
		description = "Medium Infantry Kbot",
		side = "ARM",
		unitname = "arm_t1_bot_warrior",
		objectname = "ARM_T1_BOT_Warrior.s3o",
		script = "ARM_T1_BOT_Warrior.lua",          -- walker: Lua script on the standard skeleton (was the COB)
		corpse = "ARM_T1_BOT_Warrior_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3236,
		buildcostmetal = 296,
		buildtime = 5709,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.9,
		brakerate = 0.25,
		acceleration = 0.09,
		turnrate = 1100,
		maxwaterdepth = 12,
		maxslope = 17,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 1100,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 437,
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
				name = "ARMWAR_LCANNON",
			},
			{
				name = "ARMWAR_EMG",
			},
		},
	},
}
