-- CORE_T1_VEH_Weasel (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_veh_weasel = {
		-- id
		name = "Weasel",
		description = "Scout",
		side = "CORE",
		unitname = "core_t1_veh_weasel",
		objectname = "CORE_T1_VEH_Weasel.s3o",
		corpse = "CORE_T1_VEH_Weasel_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 575,
		buildcostmetal = 38,
		buildtime = 1515,
		-- movement or placement
		movementclass = "KBOTBAD",  -- TANKSH2
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 3.2,
		brakerate = 0.051,
		acceleration = 0.1,
		turnrate = 500,
		maxwaterdepth = 12,
		maxslope = 18,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 84,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 543,
		radardistance = 700,
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		leavetracks = 1,
		trackwidth = 24,
		trackoffset = 3,
		trackstrength = 5,
		trackstretch = 1,
		tracktype = "VehTrack",
		footprintx = 2,
		footprintz = 2,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 0,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
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
				name = "CORE_SCOUT_LASER",
			},
		},
	},
}
