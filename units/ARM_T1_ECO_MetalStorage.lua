-- ARM_T1_ECO_MetalStorage (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_eco_metalstorage = {
		-- id
		name = "Metal Storage",
		description = "Increases Metal Storage by 1000",
		side = "ARM",
		unitname = "arm_t1_eco_metalstorage",
		objectname = "ARM_T1_ECO_MetalStorage",
		script = "ARM_T1_ECO_MetalStorage.lua",
		corpse = "ARM_T1_ECO_MetalStorage_dead",
		icontype = "building",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 535,
		buildcostmetal = 305,
		buildtime = 2925,
		metalstorage = 1000,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 1329,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 376,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 4096,
		ovradjust = 1,
		sounds = {
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
				"stormtl1",
			},
			underattack = "warning1",
		},
	},
}
