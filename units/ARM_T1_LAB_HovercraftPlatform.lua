-- ARM_T1_LAB_HovercraftPlatform (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_lab_hovercraftplatform = {
		-- id
		name = "Hovercraft Platform",
		description = "Builds Hovercraft",
		side = "ARM",
		unitname = "arm_t1_lab_hovercraftplatform",
		buildoptions = Shared.buildListArmHovercraftPlatform,
		objectname = "ARM_T1_LAB_HovercraftPlatform.s3o",
		buildpic = "ARM_T1_LAB_HovercraftPlatform.png",
		script = "ARM_T1_LAB_HovercraftPlatform.lua",
		corpse = "ARM_T1_LAB_HovercraftPlatform_dead",
		category = "ARM PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5277,  -- TA 3.1c (was 3277)
		buildcostmetal = 2007,  -- TA 3.1c (was 1207)
		buildtime = 18520,  -- TA 3.1c (was 11520)
		energystorage = 200,  -- TA 3.1c (was 100)
		metalstorage = 200,  -- TA 3.1c (was 100)
		-- movement or placement
		movestate = 1,
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
		maxdamage = 3005,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 220,  -- TA 3.1c (was 380)
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
			build = "hoverok1",
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
				"hoversl1",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
