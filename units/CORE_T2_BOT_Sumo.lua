-- CORE_T2_BOT_Sumo (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_bot_sumo = {
		-- id
		name = "Sumo",
		description = "Adv. Armored Assault Kbot",
		side = "CORE",
		unitname = "core_t2_bot_sumo",
		objectname = "CORE_T2_BOT_Sumo.s3o",
		buildpic = "CORE_T2_BOT_Sumo.png",
		script = "CORE_T2_BOT_Sumo.lua",
		corpse = "CORE_T2_BOT_Sumo_dead",
		category = "CORE KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5987,
		buildcostmetal = 844,
		buildtime = 10975,  -- TA 3.1c (was 14475)
		energystorage = 100,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "KBOTGOOD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 0.34,  -- TA 3.1c (was 0.35)
		brakerate = 0.1,
		acceleration = 0.04,
		turnrate = 90,
		maxwaterdepth = 12,
		maxslope = 17,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 4950,  -- TA 3.1c (was 5500)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 245,  -- TA 3.1c (was 429)
		-- other abilities
		cantbetransported = 1,
		-- unit animation
		upright = 0,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 33,
		trackoffset = 0,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "FlatFoot",
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
				name = "CORSUMO_WEAPON",
			},
		},
	},
}
