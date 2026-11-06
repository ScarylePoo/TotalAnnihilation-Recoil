-- CORE_T2_LAB_AdvancedVehiclePlant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_lab_advancedvehicleplant = {
		-- id
		name = "Adv. Vehicle Plant",
		description = "Produces Advanced Vehicles",
		side = "CORE",
		unitname = "core_t2_lab_advancedvehicleplant",
		buildoptions = Shared.buildListCoreAdvancedVehiclePlant,
		objectname = "CORE_T2_LAB_AdvancedVehiclePlant.s3o",
		buildpic = "CORE_T2_LAB_AdvancedVehiclePlant.png",
		script = "CORE_T2_LAB_AdvancedVehiclePlant.lua",
		corpse = "CORE_T2_LAB_AdvancedVehiclePlant_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3520,  -- TA 3.1c (was 8020)
		buildcostmetal = 1947,  -- TA 3.1c (was 2047)
		buildtime = 15410,  -- TA 3.1c (was 19910)
		energystorage = 200,
		metalstorage = 200,
		-- movement or placement
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 200,  -- TA 3.1c (was 240)
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 2580,  -- TA 3.1c (was 3580)
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 220,  -- TA 3.1c (was 367)
		-- unit animation
		footprintx = 8,
		footprintz = 6,
		yardmap = "oooooooo oooooooo ooccccoo ooccccoo ooccccoo ooccccoo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 1024,
		sortbias = 0,
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
