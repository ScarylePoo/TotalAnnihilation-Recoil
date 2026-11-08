-- ARM_T2_VEH_Scarab (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_scarab = {
		-- id
		name = "Scarab",
		description = "Mobile Anti Missile Defense",
		side = "ARM",
		unitname = "arm_t2_veh_scarab",
		objectname = "ARM_T2_VEH_Scarab.s3o",
		buildpic = "ARM_T2_VEH_Scarab.png",
		script = "ARM_T2_VEH_Scarab.lua",
		corpse = "ARM_T2_VEH_Scarab_dead",
		category = "ARM SPECIAL LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 88000,  -- TA 3.1c (was 58800)
		buildcostmetal = 1437,
		buildtime = 95678,  -- TA 3.1c (was 43068)
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.2,  -- TA 3.1c (was 1.4)
		brakerate = 0.027,
		acceleration = 0.015,
		turnrate = 430,  -- TA 3.1c (was 400)
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
		trackwidth = 50,
		trackoffset = 8,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "SpidTrack",
		footprintx = 3,
		footprintz = 3,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 1,
		steeringmode = 1,
		shootme = 1,
		maneuverleashlength = 640,
		ovradjust = 1,
		antiweapons = 1,
		defaultmissiontype = "Standby",
		sounds = {
			arrived = {
				"kbarmstp",
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
				"kbarmmov",
			},
			select = {
				"kbarmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARMSCAB_WEAPON",
			},
		},
	},
}
