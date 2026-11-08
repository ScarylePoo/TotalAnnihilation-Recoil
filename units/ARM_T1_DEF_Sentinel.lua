-- ARM_T1_DEF_Sentinel (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_def_sentinel = {
		-- id
		name = "Sentinel",
		description = "Heavy Laser Tower",
		side = "ARM",
		unitname = "arm_t1_def_sentinel",
		objectname = "ARM_T1_DEF_Sentinel.s3o",
		buildpic = "ARM_T1_DEF_Sentinel.png",
		script = "ARM_T1_DEF_Sentinel.lua",
		corpse = "ARM_T1_DEF_Sentinel_dead",
		category = "ARM LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5398,
		buildcostmetal = 584,
		buildtime = 9575,
		energystorage = 200,  -- TA 3.1c (was unset)
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "MEDIUM_BUILDINGEX",
		selfdestructas = "MEDIUM_BUILDING",
		-- properties
		maxdamage = 1230,  -- TA 3.1c (was 930)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 380,  -- TA 3.1c (was 635)
		-- unit animation
		footprintx = 3,
		footprintz = 3,
		yardmap = "ooo ooo ooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
		defaultmissiontype = "GUARD_NOMOVE",
		buildangle = 8192,
		ovradjust = 1,
		sounds = {
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
				"twractv3",
			},
			select = {
				"twractv3",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_TOWER_HEAVY_LASER",
			},
		},
	},
}
