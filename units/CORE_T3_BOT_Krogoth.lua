-- CORE_T3_BOT_Krogoth (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t3_bot_krogoth = {
		-- id
		name = "Krogoth",
		description = "Experimental Kbot",
		side = "CORE",
		unitname = "core_t3_bot_krogoth",
		objectname = "CORE_T3_BOT_Krogoth.s3o",
		buildpic = "CORE_T3_BOT_Krogoth.png",
		script = "CORE_T3_BOT_Krogoth.lua",
		corpse = "CORE_T3_BOT_Krogoth_dead",
		category = "CORE KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 116664,  -- TA 3.1c (was 186664)
		buildcostmetal = 29489,  -- TA 3.1c (was 36489)
		buildtime = 382193,  -- TA 3.1c (was 482193)
		-- movement or placement
		movementclass = "KROGOTH",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1,
		brakerate = 0.19,
		acceleration = 0.09,
		turnrate = 960,
		maxwaterdepth = 80,
		maxslope = 17,
		-- combat
		firestate = 2,
		nochasecategory = "VTOL",
		explodeas = "NUCLEAR_MISSILE",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 29918,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 255,  -- TA 3.1c (was 446)
		-- other abilities
		cantbetransported = 1,
		-- unit animation
		upright = 1,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 35,
		trackoffset = 0,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "FlatFoot",
		footprintx = 3,
		footprintz = 3,
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
				"krogstp1",
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
				"krogok1",
			},
			select = {
				"krogsel1",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "KROGOTH_ARM_CANNON",
			},
			{
				name = "KROGOTH_ANNIHILATOR_BEAM",
			},
			{
				name = "KROGOTH_ROCKET",
			},
		},
	},
}
