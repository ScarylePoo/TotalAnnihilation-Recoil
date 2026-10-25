-- ARM_T1_ECO_MetalExtractor (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_eco_metalextractor = {
		-- id
		name = "Metal Extractor",
		description = "Extracts Metal",
		side = "ARM",
		unitname = "arm_t1_eco_metalextractor",
		objectname = "ARM_T1_ECO_MetalExtractor",
		script = "ARM_T1_ECO_MetalExtractor.lua",
		corpse = "ARM_T1_ECO_MetalExtractor_dead",
		icontype = "building",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 521,
		buildcostmetal = 50,
		buildtime = 1800,
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
		maxdamage = 170,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 210,
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
		ovradjust = 1,
		sounds = {
			activate = "mexrun1",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "mexoff1",
			select = {
				"mexon1",
			},
			underattack = "warning1",
			working = "mexrun1",
		},
	},
}
