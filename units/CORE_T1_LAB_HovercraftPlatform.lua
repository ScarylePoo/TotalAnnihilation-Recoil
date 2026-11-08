-- CORE_T1_LAB_HovercraftPlatform (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_lab_hovercraftplatform = {
		-- id
		name = "Hovercraft Platform",
		description = "Builds Hovercraft",
		side = "CORE",
		unitname = "core_t1_lab_hovercraftplatform",
		buildoptions = Shared.buildListCoreHovercraftPlatform,
		objectname = "CORE_T1_LAB_HovercraftPlatform.s3o",
		buildpic = "CORE_T1_LAB_HovercraftPlatform.png",
		script = "CORE_T1_LAB_HovercraftPlatform.lua",
		corpse = "CORE_T1_LAB_HovercraftPlatform_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5421,  -- TA 3.1c (was 4421)
		buildcostmetal = 1793,  -- TA 3.1c (was 1193)
		buildtime = 19005,  -- TA 3.1c (was 12005)
		energystorage = 200,  -- TA 3.1c (was 100)
		metalstorage = 200,  -- TA 3.1c (was 100)
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 200,  -- TA 3.1c (was 130)
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 3356,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 240,  -- TA 3.1c (was 420)
		-- unit animation
		footprintx = 8,
		footprintz = 7,
		yardmap = "ooccccoo ooccccoo ooccccoo ooccccoo ooccccoo ooccccoo ooccccoo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		sounds = {
			build = "hoverok2",
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
				"hoversl2",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
