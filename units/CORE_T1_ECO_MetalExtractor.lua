-- CORE_T1_ECO_MetalExtractor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_eco_metalextractor = {
		-- id
		name = "Metal Extractor",
		description = "Extracts Metal",
		side = "CORE",
		unitname = "core_t1_eco_metalextractor",
		objectname = "CORE_T1_ECO_MetalExtractor.s3o",
		corpse = "CORE_T1_ECO_MetalExtractor_dead",
		icontype = "building",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 514,
		buildcostmetal = 51,
		buildtime = 1874,
		energyuse = 4,
		extractsmetal = 0.001,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		selfdestructcountdown = 1,
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 175,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 215,
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
		buildangle = 2048,
		ovradjust = 1,
		sounds = {
			activate = "mexrun2",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "mexoff2",
			select = {
				"mexon2",
			},
			underattack = "warning1",
			working = "mexrun2",
		},
	},
}
