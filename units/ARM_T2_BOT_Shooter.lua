-- ARM_T2_BOT_Shooter (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_shooter = {
		-- id
		name = "Shooter",
		description = "Sniper Kbot",
		side = "ARM",
		unitname = "arm_t2_bot_shooter",
		objectname = "ARM_T2_BOT_Shooter",
		corpse = "ARM_T2_BOT_Shooter_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 14727,
		buildcostmetal = 935,
		buildtime = 28137,
		-- movement or placement
		movementclass = "KBOTGOOD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.5,
		brakerate = 0.15,
		acceleration = 0.1,
		turnrate = 1216,
		maxwaterdepth = 22,
		maxslope = 14,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 320,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 508,
		-- other abilities
		cloakcost = 250,
		cloakcostmoving = 750,
		mincloakdistance = 40,
		-- unit animation
		upright = 1,
		-- SmoothAnim=1;
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
				name = "ARMsnipe_weapon",
			},
		},
	},
}
