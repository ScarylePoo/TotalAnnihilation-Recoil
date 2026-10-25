-- CORE_T1_SEAECO_UWMetalExtractor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seaeco_uwmetalextractor = {
		-- id
		name = "Underwater Metal Extractor",
		description = "Extracts Metal",
		side = "CORE",
		unitname = "core_t1_seaeco_uwmetalextractor",
		objectname = "CORE_T1_SEAECO_UWMetalExtractor",
		corpse = "CORE_T1_SEAECO_UWMetalExtractor_dead",
		icontype = "building",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1419,
		buildcostmetal = 95,
		buildtime = 4587,
		energyuse = 5,
		extractsmetal = 0.001,
		-- movement or placement
		minwaterdepth = 10,
		maxslope = 20,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 355,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 227,
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
