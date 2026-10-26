-- ARM_T1_SEA_Crusader (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_sea_crusader = {
		-- id
		name = "Crusader",
		description = "Destroyer",
		side = "ARM",
		unitname = "arm_t1_sea_crusader",
		objectname = "ARM_T1_SEA_Crusader.s3o",
		corpse = "ARM_T1_SEA_Crusader_dead",
		icontype = "ship",
		category = "ARM SHIP LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4237,
		buildcostmetal = 882,
		buildtime = 10391,
		-- movement or placement
		movementclass = "SMALL_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2.9,
		brakerate = 0.013,
		acceleration = 0.04,
		turnrate = 242,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1870,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 595,
		sonardistance = 455,
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		waterline = 4,
		footprintx = 4,
		footprintz = 4,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		scale = 0.5,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		buildangle = 16384,
		ovradjust = 1,
		sounds = {
			arrived = {
				"sharmstp",
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
				"sharmmov",
			},
			select = {
				"sharmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_ROY",
			},
			{
				name = "ARM_DEPTHCHARGE",
			},
		},
	},
}
