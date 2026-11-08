-- ARM_T1_LAB_SeaplanePlatform (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_lab_seaplaneplatform = {
		-- id
		name = "Seaplane Platform",
		description = "Builds Seaplanes",
		side = "ARM",
		unitname = "arm_t1_lab_seaplaneplatform",
		buildoptions = Shared.buildListArmSeaplanePlatform,
		objectname = "ARM_T1_LAB_SeaplanePlatform.s3o",
		buildpic = "ARM_T1_LAB_SeaplanePlatform.png",
		script = "ARM_T1_LAB_SeaplanePlatform.lua",
		corpse = "ARM_T1_LAB_SeaplanePlatform_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5396,
		buildcostmetal = 2223,  -- TA 3.1c (was 1663)
		buildtime = 19248,  -- TA 3.1c (was 10248)
		energystorage = 200,  -- TA 3.1c (was 100)
		metalstorage = 900,  -- TA 3.1c (was 100)
		metalmake = 1,  -- TA 3.1c (was unset)
		-- movement or placement
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		minwaterdepth = 20,  -- 30
		-- nanolathing
		builder = 1,
		workertime = 200,  -- TA 3.1c (was 110)
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 1820,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 130,  -- TA 3.1c (was 227)
		-- unit animation
		waterline = 53,
		footprintx = 7,
		footprintz = 7,
		yardmap = "wwwwwww wCCCCCw wCCCCCw wCCCCCw wCCCCCw wCCCCCw wwwwwww",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		noshadow = 1,
		ovradjust = 1,
		sounds = {
			build = "seaplok1",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			select = {
				"seaplsl1",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
