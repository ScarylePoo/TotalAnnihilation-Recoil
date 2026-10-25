-- CORE_T2_BOT_TheCan (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_thecan = {
		-- id
		name = "The Can",
		description = "Armored Assault Kbot",
		side = "CORE",
		unitname = "core_t2_bot_thecan",
		objectname = "CORE_T2_BOT_TheCan",
		corpse = "CORE_T2_BOT_TheCan_dead",
		icontype = "kbot",
		category = "CORE KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3500,
		buildcostmetal = 420,
		buildtime = 8126,
		-- movement or placement
		movementclass = "KBOTBAD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 0.8,
		brakerate = 0.15,
		acceleration = 0.1,
		turnrate = 940,
		maxwaterdepth = 21,
		maxslope = 14,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 3200,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 350,
		-- unit animation
		upright = 1,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 28,
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
				name = "CORE_CANLASER",
			},
		},
	},
}
