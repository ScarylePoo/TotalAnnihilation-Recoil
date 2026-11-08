-- ARM_T2_LAB_AdvancedAircraftPlant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_lab_advancedaircraftplant = {
		-- id
		name = "Adv. Aircraft Plant",
		description = "Produces Advanced Aircraft",
		side = "ARM",
		unitname = "arm_t2_lab_advancedaircraftplant",
		buildoptions = Shared.buildListArmAdvancedAircraftPlant,
		objectname = "ARM_T2_LAB_AdvancedAircraftPlant.s3o",
		buildpic = "ARM_T2_LAB_AdvancedAircraftPlant.png",
		script = "ARM_T2_LAB_AdvancedAircraftPlant.lua",
		corpse = "ARM_T2_LAB_AdvancedAircraftPlant_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4521,  -- TA 3.1c (was 16521)
		buildcostmetal = 2210,  -- TA 3.1c (was 2510)
		buildtime = 17376,  -- TA 3.1c (was 21376)
		energystorage = 200,
		metalstorage = 200,
		radardistance = 1200,  -- TA 3.1c (was unset)
		-- movement or placement
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 200,  -- TA 3.1c (was 220)
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 2100,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 240,  -- TA 3.1c (was 420)
		-- unit animation
		footprintx = 7,
		footprintz = 6,
		yardmap = "ooooooo ooooooo occccco occccco occccco occccco",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		ovradjust = 1,
		sounds = {
			build = "pairwork",
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
				"pairactv",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
