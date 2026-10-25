-- CORE_T1_LAB_SeaplanePlatform (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_lab_seaplaneplatform = {
		-- id
		name = "Seaplane Platform",
		description = "Builds Seaplanes",
		side = "CORE",
		unitname = "core_t1_lab_seaplaneplatform",
		buildoptions = Shared.buildListCoreSeaplanePlatform,
		objectname = "CORE_T1_LAB_SeaplanePlatform",
		corpse = "CORE_T1_LAB_SeaplanePlatform_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5367,
		buildcostmetal = 1695,
		buildtime = 10102,
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
		maxdamage = 2000,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 228,
		-- unit animation
		waterline = 43,
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
			build = "seaplok2",
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
				"seaplsl2",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
