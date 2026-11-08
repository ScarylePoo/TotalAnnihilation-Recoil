-- CORE_T2_VEH_Crock (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_veh_crock = {
		-- id
		name = "Crock",
		description = "Amphibious Tank",
		side = "CORE",
		unitname = "core_t2_veh_crock",
		objectname = "CORE_T2_VEH_Crock.s3o",
		buildpic = "CORE_T2_VEH_Crock.png",
		script = "CORE_T2_VEH_Crock.lua",
		corpse = "CORE_T2_VEH_Crock_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2310,  -- TA 3.1c (was 2910)
		buildcostmetal = 295,  -- TA 3.1c (was 350)
		buildtime = 6119,
		-- movement or placement
		movementclass = "AMPHTANK",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.2,  -- TA 3.1c (was 1.4)
		brakerate = 0.008,
		acceleration = 0.008,  -- TA 3.1c (was 0.01)
		turnrate = 320,
		maxwaterdepth = 255,
		maxslope = 16,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1144,  -- TA 3.1c (was 2044)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 230,  -- TA 3.1c (was 400)
		-- unit animation
		leavetracks = 1,
		trackwidth = 40,
		trackoffset = 8,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "VehTrack",
		footprintx = 2,
		footprintz = 2,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
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
				name = "CORE_MEDIUMCANNON",
			},
		},
	},
}
