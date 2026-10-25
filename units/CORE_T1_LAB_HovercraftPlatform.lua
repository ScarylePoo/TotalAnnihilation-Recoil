-- CORE_T1_LAB_HovercraftPlatform (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_lab_hovercraftplatform = {
		-- id
		name = "Hovercraft Platform",
		description = "Builds Hovercraft",
		side = "CORE",
		unitname = "core_t1_lab_hovercraftplatform",
		buildoptions = Shared.buildListCoreHovercraftPlatform,
		objectname = "CORE_T1_LAB_HovercraftPlatform",
		corpse = "CORE_T1_LAB_HovercraftPlatform_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4421,
		buildcostmetal = 1193,
		buildtime = 12005,
		energystorage = 100,
		metalstorage = 100,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 130,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 3356,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 420,
		-- unit animation
		footprintx = 8,
		footprintz = 7,
		yardmap = "ooccccoo ooccccoo ooccccoo ooccccoo ooccccoo ooccccoo ooccccoo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		sounds = {
			build = "hoverok2",
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
				"hoversl2",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
