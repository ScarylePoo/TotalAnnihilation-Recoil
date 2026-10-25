-- CORE_T2_VEH_Copperhead (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_veh_copperhead = {
		-- id
		name = "Copperhead",
		description = "Mobile Flak Vehicle",
		side = "CORE",
		unitname = "core_t2_veh_copperhead",
		objectname = "CORE_T2_VEH_Copperhead.s3o",
		corpse = "CORE_T2_VEH_Copperhead_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 12487,
		buildcostmetal = 886,
		buildtime = 23975,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.3,
		brakerate = 0.1,
		acceleration = 0.04,
		turnrate = 489,
		maxwaterdepth = 12,
		maxslope = 14,
		-- combat
		firestate = 2,
		nochasecategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 685,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 455,
		-- unit animation
		leavetracks = 1,
		trackwidth = 33,
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
		steeringmode = 2,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 30,
		ovradjust = 1,
		sounds = {
			arrived = {
				"tcorst0p",
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
				"tcormove",
			},
			select = {
				"tcorsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORSENT_GUN",
				onlytargetcategory = "VTOL",
			},
		},
	},
}
