-- ARM_T1_LAB_VehiclePlant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_lab_vehicleplant = {
		-- id
		name = "Vehicle Plant",
		description = "Produces Vehicles",
		side = "ARM",
		unitname = "arm_t1_lab_vehicleplant",
		buildoptions = Shared.buildListArmVehiclePlant,
		objectname = "ARM_T1_LAB_VehiclePlant.s3o",
		buildpic = "ARM_T1_LAB_VehiclePlant.png",
		script = "ARM_T1_LAB_VehiclePlant.lua",
		corpse = "ARM_T1_LAB_VehiclePlant_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1000,  -- TA 3.1c (was 978)
		buildcostmetal = 620,  -- TA 3.1c (was 671)
		buildtime = 6500,  -- TA 3.1c (was 6493)
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
		workertime = 100,  -- TA 3.1c (was 120)
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 2580,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 210,  -- TA 3.1c (was 365)
		-- unit animation
		footprintx = 8,
		footprintz = 6,
		yardmap = "oooooooo ooccccoo ooccccoo ooccccoo ooccccoo ooccccoo",
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
