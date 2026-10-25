-- ARM_T1_SEAECO_UWMetalStorage (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seaeco_uwmetalstorage = {
		-- id
		name = "Underwater Metal Storage",
		description = "Increases Metal Storage by 1500",
		side = "ARM",
		unitname = "arm_t1_seaeco_uwmetalstorage",
		objectname = "ARM_T1_SEAECO_UWMetalStorage",
		script = "ARM_T1_SEAECO_UWMetalStorage.lua",
		corpse = "ARM_T1_SEAECO_UWMetalStorage_dead",
		icontype = "building",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1255,
		buildcostmetal = 360,
		buildtime = 3741,
		metalstorage = 1500,
		-- movement or placement
		minwaterdepth = 31,
		maxslope = 20,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 1625,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 245,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
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
