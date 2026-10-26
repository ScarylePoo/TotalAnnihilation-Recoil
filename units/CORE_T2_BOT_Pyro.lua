-- CORE_T2_BOT_Pyro (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_pyro = {
		-- id
		name = "Pyro",
		description = "Assault Kbot",
		side = "CORE",
		unitname = "core_t2_bot_pyro",
		objectname = "CORE_T2_BOT_Pyro.s3o",
		script = "CORE_T2_BOT_Pyro.lua",
		corpse = "CORE_T2_BOT_Pyro_dead",
		icontype = "kbot",
		category = "CORE KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1600,  -- 2200
		buildcostmetal = 210,  -- 260
		buildtime = 3750,
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.7,
		brakerate = 0.18,
		acceleration = 0.1,
		turnrate = 950,
		maxwaterdepth = 25,
		maxslope = 17,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "CORPYRO_BLAST",
		selfdestructas = "CORPYRO_SUICIDE",
		-- properties
		maxdamage = 700,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 429,
		-- unit animation
		upright = 1,
		smoothanim = 1,
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
				name = "FLAMETHROWER",
			},
		},
	},
}
