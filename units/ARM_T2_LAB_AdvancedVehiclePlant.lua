-- ARM_T2_LAB_AdvancedVehiclePlant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_lab_advancedvehicleplant = {
		-- id
		name = "Adv. Vehicle Plant",
		description = "Produces Advanced Vehicles",
		side = "ARM",
		unitname = "arm_t2_lab_advancedvehicleplant",
		buildoptions = Shared.buildListArmAdvancedVehiclePlant,
		objectname = "ARM_T2_LAB_AdvancedVehiclePlant.s3o",
		buildpic = "ARM_T2_LAB_AdvancedVehiclePlant.png",
		script = "ARM_T2_LAB_AdvancedVehiclePlant.lua",
		corpse = "ARM_T2_LAB_AdvancedVehiclePlant_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3200,  -- TA 3.1c (was 8235)
		buildcostmetal = 1984,
		buildtime = 14950,  -- TA 3.1c (was 19350)
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
		maxdamage = 2435,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 218,  -- TA 3.1c (was 380)
		-- unit animation
		footprintx = 6,
		footprintz = 6,
		yardmap = "occcco occcco occcco occcco occcco occcco",
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
