-- CORE_T1_DEF_Punisher (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_def_punisher = {
		-- id
		name = "Punisher",
		description = "Plasma Battery",
		side = "CORE",
		unitname = "core_t1_def_punisher",
		objectname = "CORE_T1_DEF_Punisher.s3o",
		buildpic = "CORE_T1_DEF_Punisher.png",
		script = "CORE_T1_DEF_Punisher.lua",
		corpse = "CORE_T1_DEF_Punisher_dead",
		icontype = "turret",
		category = "CORE LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7585,
		buildcostmetal = 1887,
		buildtime = 13268,  -- TA 3.1c (was 16268)
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
		maxdamage = 2540,
		hidedamage = 1,
		iidletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 350,  -- TA 3.1c (was 612)
		-- unit animation
		footprintx = 4,
		footprintz = 3,
		yardmap = "oooo oooo oooo",
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
			arrived = {
				"kbcorstp",
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
				"kbcormov",
			},
			select = {
				"kbcorsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORFIXED_GUN",
			},
		},
	},
}
