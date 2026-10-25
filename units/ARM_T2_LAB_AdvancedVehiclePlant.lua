-- ARM_T2_LAB_AdvancedVehiclePlant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_lab_advancedvehicleplant = {
		-- id
		name = "Adv. Vehicle Plant",
		description = "Produces Advanced Vehicles",
		side = "ARM",
		unitname = "arm_t2_lab_advancedvehicleplant",
		buildoptions = Shared.buildListArmAdvancedVehiclePlant,
		objectname = "ARM_T2_LAB_AdvancedVehiclePlant",
		corpse = "ARM_T2_LAB_AdvancedVehiclePlant_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 8235,
		buildcostmetal = 1984,
		buildtime = 19350,
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
		workertime = 240,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 2435,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 380,
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
