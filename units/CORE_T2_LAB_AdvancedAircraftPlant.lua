-- CORE_T2_LAB_AdvancedAircraftPlant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_lab_advancedaircraftplant = {
		-- id
		name = "Adv. Aircraft Plant",
		description = "Produces Advanced Aircraft",
		side = "CORE",
		unitname = "core_t2_lab_advancedaircraftplant",
		buildoptions = Shared.buildListCoreAdvancedAircraftPlant,
		objectname = "CORE_T2_LAB_AdvancedAircraftPlant.s3o",
		buildpic = "CORE_T2_LAB_AdvancedAircraftPlant.png",
		script = "CORE_T2_LAB_AdvancedAircraftPlant.lua",
		corpse = "CORE_T2_LAB_AdvancedAircraftPlant_dead",
		category = "CORE PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4422,  -- TA 3.1c (was 15422)
		buildcostmetal = 2191,  -- TA 3.1c (was 2491)
		buildtime = 17232,  -- TA 3.1c (was 21232)
		energystorage = 200,
		metalstorage = 200,
		radardistance = 1150,  -- TA 3.1c (was unset)
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
		maxdamage = 2200,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 235,  -- TA 3.1c (was 411)
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
