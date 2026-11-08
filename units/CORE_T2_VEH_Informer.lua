-- CORE_T2_VEH_Informer (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_veh_informer = {
		-- id
		name = "Informer",
		description = "Mobile Radar",
		side = "CORE",
		unitname = "core_t2_veh_informer",
		objectname = "CORE_T2_VEH_Informer.s3o",
		buildpic = "CORE_T2_VEH_Informer.png",
		script = "CORE_T2_VEH_Informer.lua",
		corpse = "CORE_T2_VEH_Informer_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1209,
		buildcostmetal = 86,
		buildtime = 4223,
		energyuse = 11,
		energymake = 11,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.4,  -- TA 3.1c (was 1.6)
		brakerate = 0.012,
		acceleration = 0.03,
		turnrate = 210,
		maxwaterdepth = 0,
		maxslope = 16,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 510,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 210,  -- TA 3.1c (was 367)
		radardistance = 1120,  -- TA 3.1c (was 1750)
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		leavetracks = 1,
		trackwidth = 20,
		trackoffset = 0,
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
	},
}
