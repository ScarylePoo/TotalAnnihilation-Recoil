-- ARM_T2_BOT_Fido (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_fido = {
		-- id
		name = "Fido",
		description = "Assault Kbot",
		side = "ARM",
		unitname = "arm_t2_bot_fido",
		objectname = "ARM_T2_BOT_Fido.s3o",
		buildpic = "ARM_T2_BOT_Fido.png",
		script = "ARM_T2_BOT_Fido.lua",
		corpse = "ARM_T2_BOT_Fido_dead",
		category = "ARM KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3556,  -- TA 3.1c (was 2556)
		buildcostmetal = 398,  -- TA 3.1c (was 358)
		buildtime = 10827,  -- TA 3.1c (was 9227)
		-- movement or placement
		movementclass = "KBOTBAD",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.75,  -- TA 3.1c (was 2.1)
		brakerate = 0.3,
		acceleration = 0.1,  -- TA 3.1c (was 0.27)
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
		maxdamage = 1000,  -- TA 3.1c (was 900)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 245,  -- TA 3.1c (was 429)
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
