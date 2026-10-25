-- ARM_T2_BOT_Pelican (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_pelican = {
		-- id
		name = "Pelican",
		description = "Amphibious Kbot",
		side = "ARM",
		unitname = "arm_t2_bot_pelican",
		objectname = "ARM_T2_BOT_Pelican",
		corpse = "ARM_T2_BOT_Pelican_dead",
		icontype = "kbot",
		category = "ARM KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2468,
		buildcostmetal = 255,
		buildtime = 5582,
		-- movement or placement
		movementclass = "TANKHOVER3",
		movestate = -1,
		floater = 0,
		canhover = 1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.9,
		brakerate = 0.35,
		acceleration = 0.2,
		turnrate = 400,
		maxslope = 25,
		-- combat
		firestate = 2,
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 800,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 508,
		-- unit animation
		upright = 1,
		smoothanim = 1,
		waterline = 4,
		leavetracks = 1,
		trackwidth = 22,
		trackoffset = 0,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "KbotTrack",
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
		noshadow = 1,
		sounds = {
			arrived = {
				"amphstp1",
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
				"amphok1",
			},
			select = {
				"amphsel1",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				badtargetcategory = "VTOL",
				name = "ARM_PELICAN_LASER",
			},
			{
				name = "ARMAMPH_WEAPON2",
				onlytargetcategory = "VTOL",
			},
		},
	},
}
