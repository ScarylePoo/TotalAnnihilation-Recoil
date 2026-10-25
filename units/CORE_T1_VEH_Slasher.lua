-- CORE_T1_VEH_Slasher (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_veh_slasher = {
		-- id
		name = "Slasher",
		description = "Missile Launcher",
		side = "CORE",
		unitname = "core_t1_veh_slasher",
		objectname = "CORE_T1_VEH_Slasher.s3o",
		corpse = "CORE_T1_VEH_Slasher_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 947,
		buildcostmetal = 116,
		buildtime = 1820,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.5,
		brakerate = 0.012,
		acceleration = 0.03,
		turnrate = 512,
		maxwaterdepth = 12,
		maxslope = 16,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 375,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 400,
		-- unit animation
		leavetracks = 1,
		trackwidth = 26,
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
				"vcorstop",
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
				"vcormove",
			},
			select = {
				"vcorsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORTRUCK_MISSILE",
			},
		},
	},
}
