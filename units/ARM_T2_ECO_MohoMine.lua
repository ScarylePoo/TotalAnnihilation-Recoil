-- ARM_T2_ECO_MohoMine (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_eco_mohomine = {
		-- id
		name = "Moho Mine",
		description = "Advanced Metal Extractor",
		side = "ARM",
		unitname = "arm_t2_eco_mohomine",
		objectname = "ARM_T2_ECO_MohoMine",
		corpse = "ARM_T2_ECO_MohoMine_dead",
		icontype = "building_metal_source_big",
		category = "ARM LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 8700,
		buildcostmetal = 1508,
		buildtime = 23150,
		energyuse = 24,
		extractsmetal = 0.005,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 1573,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 376,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		footprintx = 5,
		footprintz = 5,
		yardmap = "ooooo ooooo ooooo ooooo ooooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 2048,
		ovradjust = 1,
		sounds = {
			activate = "mohorun1",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "mohooff1",
			select = {
				"mohoon1",
			},
			underattack = "warning1",
			working = "mohorun1",
		},
	},
}
