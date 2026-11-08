-- CORE_T2_VEH_Hedgehog (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_veh_hedgehog = {
		-- id
		name = "Hedgehog",
		description = "Mobile Anti Missile Defense",
		side = "CORE",
		unitname = "core_t2_veh_hedgehog",
		objectname = "CORE_T2_VEH_Hedgehog.s3o",
		buildpic = "CORE_T2_VEH_Hedgehog.png",
		script = "CORE_T2_VEH_Hedgehog.lua",
		corpse = "CORE_T2_VEH_Hedgehog_dead",
		category = "CORE SPECIAL LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 92321,  -- TA 3.1c (was 62320)
		buildcostmetal = 1508,
		buildtime = 96450,  -- TA 3.1c (was 43500)
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.2,  -- TA 3.1c (was 1.4)
		brakerate = 0.027,
		acceleration = 0.015,
		turnrate = 430,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "CRAWL_BLASTSML",
		-- properties
		maxdamage = 780,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 155,  -- TA 3.1c (was 271)
		-- other abilities
		damagemodifier = 0.5,
		-- unit animation
		leavetracks = 1,
		trackwidth = 34,
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
		noautofire = 1,
		ovradjust = 1,
		steeringmode = 1,
		shootme = 1,
		maneuverleashlength = 640,
		antiweapons = 1,
		defaultmissiontype = "Standby",
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
				name = "CORMABM_WEAPON",
			},
		},
	},
}
