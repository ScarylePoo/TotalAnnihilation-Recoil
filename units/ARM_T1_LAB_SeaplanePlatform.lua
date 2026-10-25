-- ARM_T1_LAB_SeaplanePlatform (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_lab_seaplaneplatform = {
		-- id
		name = "Seaplane Platform",
		description = "Builds Seaplanes",
		side = "ARM",
		unitname = "arm_t1_lab_seaplaneplatform",
		buildoptions = Shared.buildListArmSeaplanePlatform,
		objectname = "ARM_T1_LAB_SeaplanePlatform",
		corpse = "ARM_T1_LAB_SeaplanePlatform_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5396,
		buildcostmetal = 1663,
		buildtime = 10248,
		energystorage = 100,
		metalstorage = 100,
		-- movement or placement
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		minwaterdepth = 20,  -- 30
		-- nanolathing
		builder = 1,
		workertime = 110,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 1820,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 227,
		-- unit animation
		waterline = 53,
		footprintx = 7,
		footprintz = 7,
		yardmap = "wwwwwww wCCCCCw wCCCCCw wCCCCCw wCCCCCw wCCCCCw wwwwwww",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		noshadow = 1,
		ovradjust = 1,
		sounds = {
			build = "seaplok1",
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
				"seaplsl1",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
