-- ARM_T2_LAB_AdvancedShipyard (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_lab_advancedshipyard = {
		-- id
		name = "Adv. Shipyard",
		description = "Produces Advanced Ships",
		side = "ARM",
		unitname = "arm_t2_lab_advancedshipyard",
		buildoptions = Shared.buildListArmAdvancedShipyard,
		objectname = "ARM_T2_LAB_AdvancedShipyard.s3o",
		buildpic = "ARM_T2_LAB_AdvancedShipyard.png",
		script = "ARM_T2_LAB_AdvancedShipyard.lua",
		corpse = "ARM_T2_LAB_AdvancedShipyard_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2402,  -- TA 3.1c (was 12402)
		buildcostmetal = 2524,  -- TA 3.1c (was 2724)
		buildtime = 13310,  -- TA 3.1c (was 16310)
		energystorage = 200,
		metalstorage = 200,
		metalmake = 1,  -- TA 3.1c (was unset)
		-- movement or placement
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		minwaterdepth = 30,
		-- nanolathing
		builder = 1,
		workertime = 200,  -- TA 3.1c (was 280)
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 2820,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 230,  -- TA 3.1c (was 400)
		-- unit animation
		waterline = 1,
		footprintx = 8,
		footprintz = 8,
		yardmap = "wCCCCCCw CCCCCCCC CCCCCCCC CCCCCCCC CCCCCCCC CCCCCCCC CCCCCCCC wCCCCCCw",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		noshadow = 1,
		ovradjust = 1,
		sounds = {
			build = "pshpwork",
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
				"pshpactv",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
