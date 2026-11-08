-- CORE_T3_LAB_KrogothGantry (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t3_lab_krogothgantry = {
		-- id
		name = "Krogoth Gantry",
		description = "Builds Krogoth",
		side = "CORE",
		unitname = "core_t3_lab_krogothgantry",
		buildoptions = Shared.buildListCoreKrogothGantry,
		objectname = "CORE_T3_LAB_KrogothGantry.s3o",
		buildpic = "CORE_T3_LAB_KrogothGantry.png",
		script = "CORE_T3_LAB_KrogothGantry.lua",
		corpse = "CORE_T3_LAB_KrogothGantry_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 9574,  -- TA 3.1c (was 29574)
		buildcostmetal = 6587,  -- TA 3.1c (was 6087)
		buildtime = 41937,  -- TA 3.1c (was 61937)
		energystorage = 1400,  -- TA 3.1c (was 400)
		metalstorage = 800,  -- TA 3.1c (was 400)
		-- movement or placement
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 200,  -- TA 3.1c (was 260)
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 3050,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 210,  -- TA 3.1c (was 367)
		-- unit animation
		footprintx = 9,
		footprintz = 9,
		yardmap = "ooooooooo ooooooooo oocccccoo oocccccoo oocccccoo oocccccoo oocccccoo oocccccoo oocccccoo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		sounds = {
			activate = "gantok2",
			build = "gantok2",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "gantok2",
			repair = "lathelrg",
			select = {
				"gantsel1",
			},
			underattack = "warning1",
			unitcomplete = "gantok1",
			working = "build",
		},
	},
}
