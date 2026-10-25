-- CORE_T1_ECO_MetalStorage (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_eco_metalstorage = {
		-- id
		name = "Metal Storage",
		description = "Increases Metal Storage by 1000",
		side = "CORE",
		unitname = "core_t1_eco_metalstorage",
		objectname = "CORE_T1_ECO_MetalStorage",
		corpse = "CORE_T1_ECO_MetalStorage_dead",
		icontype = "building",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 550,
		buildcostmetal = 320,
		buildtime = 2925,
		metalstorage = 1000,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 1306,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- unit animation
		footprintx = 5,
		footprintz = 5,
		yardmap = "ooooo ooooo ooooo ooooo ooooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
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
				"stormtl2",
			},
			underattack = "warning1",
		},
	},
}
