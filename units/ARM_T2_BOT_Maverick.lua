-- ARM_T2_BOT_Maverick (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_maverick = {
		-- id
		name = "Maverick",
		description = "Gun-slinging Kbot",
		side = "ARM",
		unitname = "arm_t2_bot_maverick",
		objectname = "ARM_T2_BOT_Maverick.s3o",
		buildpic = "ARM_T2_BOT_Maverick.png",
		script = "ARM_T2_BOT_Maverick.lua",
		corpse = "ARM_T2_BOT_Maverick_dead",
		category = "ARM KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 10914,  -- TA 3.1c (was 8814)
		buildcostmetal = 492,
		buildtime = 24850,  -- TA 3.1c (was 12850)
		-- movement or placement
		movementclass = "KBOTSTANDARD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.4,  -- TA 3.1c (was 1.6)
		brakerate = 0.15,
		acceleration = 0.1,
		turnrate = 1016,
		maxwaterdepth = 0,
		maxslope = 14,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 870,  -- TA 3.1c (was 950)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 290,  -- TA 3.1c (was 507)
		-- unit animation
		upright = 1,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 22,
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
				"mavbok1",
			},
			select = {
				"mavbsel1",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "Armmav_weapon",
			},
		},
	},
}
