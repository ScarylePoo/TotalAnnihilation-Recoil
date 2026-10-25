-- CORE_T3_LAB_KrogothGantry (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t3_lab_krogothgantry = {
		-- id
		name = "Krogoth Gantry",
		description = "Builds Krogoth",
		side = "CORE",
		unitname = "core_t3_lab_krogothgantry",
		buildoptions = Shared.buildListCoreKrogothGantry,
		objectname = "CORE_T3_LAB_KrogothGantry",
		corpse = "CORE_T3_LAB_KrogothGantry_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 29574,
		buildcostmetal = 6087,
		buildtime = 61937,
		energystorage = 400,
		metalstorage = 400,
		-- movement or placement
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 260,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 3050,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- unit animation
		footprintx = 9,
		footprintz = 9,
		yardmap = "ooooooooo ooooooooo oocccccoo oocccccoo oocccccoo oocccccoo oocccccoo oocccccoo oocccccoo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		sounds = {
			activate = "gantok2",
			build = "gantok2",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "gantok2",
			repair = "lathelrg",
			select = {
				"gantsel1",
			},
			underattack = "warning1",
			unitcomplete = "gantok1",
			working = "build",
		},
	},
}
