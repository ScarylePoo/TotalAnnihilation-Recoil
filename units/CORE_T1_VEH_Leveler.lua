-- CORE_T1_VEH_Leveler (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_veh_leveler = {
		-- id
		name = "Leveler",
		description = "Riot Tank",
		side = "CORE",
		unitname = "core_t1_veh_leveler",
		objectname = "CORE_T1_VEH_Leveler.s3o",
		buildpic = "CORE_T1_VEH_Leveler.png",
		script = "CORE_T1_VEH_Leveler.lua",
		corpse = "CORE_T1_VEH_Leveler_dead",
		category = "CORE TANK LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1887,
		buildcostmetal = 292,
		buildtime = 4209,
		-- movement or placement
		movementclass = "TANKSH2",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 0.8,  -- TA 3.1c (was 1)
		brakerate = 0.19,
		acceleration = 0.02,
		turnrate = 220,
		maxwaterdepth = 12,
		maxslope = 17,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "MEDIUM_UNIT",
		-- properties
		maxdamage = 375,  -- TA 3.1c (was 425)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 220,  -- TA 3.1c (was 385)
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
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 2,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
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
				name = "CORLEVLR_WEAPON",
			},
		},
	},
}
