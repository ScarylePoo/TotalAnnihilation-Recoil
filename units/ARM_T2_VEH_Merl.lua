-- ARM_T2_VEH_Merl (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_merl = {
		-- id
		name = "Merl",
		description = "Mobile Rocket Launcher",
		side = "ARM",
		unitname = "arm_t2_veh_merl",
		objectname = "ARM_T2_VEH_Merl",
		corpse = "ARM_T2_VEH_Merl_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2746,
		buildcostmetal = 462,
		buildtime = 8592,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.3,
		brakerate = 0.029,
		acceleration = 0.017,
		turnrate = 430,
		maxwaterdepth = 12,
		maxslope = 16,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 540,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 410,
		-- unit animation
		leavetracks = 1,
		trackwidth = 40,
		trackoffset = 8,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "VehTrack",
		footprintx = 3,
		footprintz = 3,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		ovradjust = 1,
		sounds = {
			arrived = {
				"varmstop",
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
				"varmmove",
			},
			select = {
				"varmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_VEH_ROCKET",
				onlytargetcategory = "NOTAIR",
			},
		},
	},
}
