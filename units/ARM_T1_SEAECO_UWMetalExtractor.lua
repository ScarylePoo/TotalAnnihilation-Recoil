-- ARM_T1_SEAECO_UWMetalExtractor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seaeco_uwmetalextractor = {
		-- id
		name = "Underwater Metal Extractor",
		description = "Extracts Metal",
		side = "ARM",
		unitname = "arm_t1_seaeco_uwmetalextractor",
		objectname = "ARM_T1_SEAECO_UWMetalExtractor.s3o",
		buildpic = "ARM_T1_SEAECO_UWMetalExtractor.png",
		script = "ARM_T1_SEAECO_UWMetalExtractor.lua",
		corpse = "ARM_T1_SEAECO_UWMetalExtractor_dead",
		icontype = "building",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2074,  -- TA 3.1c (was 1274)
		buildcostmetal = 130,  -- TA 3.1c (was 97)
		buildtime = 4175,
		energyuse = 2,  -- TA 3.1c (was 5)
		extractsmetal = 0.001,
		-- movement or placement
		minwaterdepth = 19,
		maxslope = 24,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 330,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 140,  -- TA 3.1c (was 245)
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		footprintx = 3,
		footprintz = 3,
		yardmap = "ooo ooo ooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
		sounds = {
			activate = "waterex1",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "waterex1",
			select = {
				"waterex1",
			},
			underattack = "warning1",
			working = "waterex1",
		},
	},
}
