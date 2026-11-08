-- CORE_T1_SEAECO_UWMetalExtractor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seaeco_uwmetalextractor = {
		-- id
		name = "Underwater Metal Extractor",
		description = "Extracts Metal",
		side = "CORE",
		unitname = "core_t1_seaeco_uwmetalextractor",
		objectname = "CORE_T1_SEAECO_UWMetalExtractor.s3o",
		buildpic = "CORE_T1_SEAECO_UWMetalExtractor.png",
		script = "CORE_T1_SEAECO_UWMetalExtractor.lua",
		corpse = "CORE_T1_SEAECO_UWMetalExtractor_dead",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2219,  -- TA 3.1c (was 1419)
		buildcostmetal = 125,  -- TA 3.1c (was 95)
		buildtime = 4587,
		energyuse = 2,  -- TA 3.1c (was 5)
		extractsmetal = 0.001,
		-- movement or placement
		minwaterdepth = 10,
		maxslope = 20,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 355,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 130,  -- TA 3.1c (was 227)
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
			activate = "waterex2",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "waterex2",
			select = {
				"waterex2",
			},
			underattack = "warning1",
			working = "waterex2",
		},
	},
}
