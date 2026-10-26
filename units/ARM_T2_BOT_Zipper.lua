-- ARM_T2_BOT_Zipper (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_zipper = {
		-- id
		name = "Zipper",
		description = "Fast Attack Kbot",
		side = "ARM",
		unitname = "arm_t2_bot_zipper",
		objectname = "ARM_T2_BOT_Zipper.s3o",
		script = "ARM_T2_BOT_Zipper.lua",
		corpse = "ARM_T2_BOT_Zipper_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2221,
		buildcostmetal = 151,
		buildtime = 6768,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 3.93,
		brakerate = 0.27,
		acceleration = 0.18,
		turnrate = 1300,
		maxwaterdepth = 12,
		maxslope = 17,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 550,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 460,
		-- unit animation
		upright = 1,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 12,
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
				name = "ARM_ZIPPER_LASER",
			},
		},
	},
}
