-- CORE_T2_BOT_Morty (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_morty = {
		-- id
		name = "Morty",
		description = "Mobile Mortar Kbot",
		side = "CORE",
		unitname = "core_t2_bot_morty",
		objectname = "CORE_T2_BOT_Morty.s3o",
		corpse = "CORE_T2_BOT_Morty_dead",
		icontype = "kbot",
		category = "CORE KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2865,
		buildcostmetal = 321,
		buildtime = 7527,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.4,
		brakerate = 0.3,
		acceleration = 0.21,
		turnrate = 999,
		maxwaterdepth = 12,
		maxslope = 14,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 920,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 393,
		-- unit animation
		upright = 1,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 15,
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
			{
				name = "CORE_MORT",
			},
		},
	},
}
