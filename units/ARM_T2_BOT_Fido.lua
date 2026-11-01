-- ARM_T2_BOT_Fido (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_fido = {
		-- id
		name = "Fido",
		description = "Assault Kbot",
		side = "ARM",
		unitname = "arm_t2_bot_fido",
		objectname = "ARM_T2_BOT_Fido.s3o",
		script = "ARM_T2_BOT_Fido.lua",
		corpse = "ARM_T2_BOT_Fido_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2556,
		buildcostmetal = 358,
		buildtime = 9227,
		-- movement or placement
		movementclass = "KBOTBAD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.1,
		brakerate = 0.3,
		acceleration = 0.27,
		turnrate = 900,
		maxwaterdepth = 12,
		maxslope = 14,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 900,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 429,
		-- unit animation
		upright = 0,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 22,
		trackoffset = 10,
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
				name = "GAUSS",
			},
		},
	},
}
