-- CORE_T2_VEH_Goliath (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_veh_goliath = {
		-- id
		name = "Goliath",
		description = "Very Heavy Assault Tank",
		side = "CORE",
		unitname = "core_t2_veh_goliath",
		objectname = "CORE_T2_VEH_Goliath.s3o",
		buildpic = "CORE_T2_VEH_Goliath.png",
		script = "CORE_T2_VEH_Goliath.lua",
		corpse = "CORE_T2_VEH_Goliath_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3906,  -- TA 3.1c (was 5906)
		buildcostmetal = 697,  -- TA 3.1c (was 1097)
		buildtime = 7058,  -- TA 3.1c (was 11058)
		-- movement or placement
		movementclass = "GOLIATH",  -- HEAVYTANK//TANKSH3
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 0.8,  -- TA 3.1c (was 1)
		brakerate = 0.03,
		acceleration = 0.015,
		turnrate = 206,
		maxwaterdepth = 12,
		maxslope = 16,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 2845,  -- TA 3.1c (was 3650)
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		mass = 3001,  -- Valkyrie limit is 3000
		sightdistance = 210,  -- TA 3.1c (was 420)
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
				name = "COR_GOL",
			},
		},
	},
}
