-- CORE_T1_LAB_VehiclePlant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_lab_vehicleplant = {
		-- id
		name = "Vehicle Plant",
		description = "Produces Vehicles",
		side = "CORE",
		unitname = "core_t1_lab_vehicleplant",
		buildoptions = Shared.buildListCoreVehiclePlant,
		objectname = "CORE_T1_LAB_VehiclePlant.s3o",
		corpse = "CORE_T1_LAB_VehiclePlant_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1100,
		buildcostmetal = 709,
		buildtime = 6687,
		energystorage = 100,
		metalstorage = 100,
		-- movement or placement
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 120,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 2550,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 380,
		-- unit animation
		footprintx = 7,
		footprintz = 7,
		yardmap = "yyoooyy yyoooyy ooooooo oocccoo oocccoo oocccoo oocccoo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 2048,
		ovradjust = 1,
		sounds = {
			build = "pvehwork",
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
				"pvehactv",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
