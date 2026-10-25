-- ARM_T1_VEH_Samson (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_veh_samson = {
		-- id
		name = "Samson",
		description = "Mobile Missile Launcher",
		side = "ARM",
		unitname = "arm_t1_veh_samson",
		objectname = "ARM_T1_VEH_Samson",
		corpse = "ARM_T1_VEH_Samson_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1027,
		buildcostmetal = 129,
		buildtime = 2066,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.6,
		brakerate = 0.022,
		acceleration = 0.03,
		turnrate = 511,
		maxwaterdepth = 12,
		maxslope = 16,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 350,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 411,
		-- unit animation
		leavetracks = 1,
		trackwidth = 24,
		trackoffset = 3,
		trackstrength = 5,
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
				name = "ARMTRUCK_MISSILE",
			},
		},
	},
}
