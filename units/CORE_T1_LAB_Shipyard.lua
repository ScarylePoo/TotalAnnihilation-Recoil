-- CORE_T1_LAB_Shipyard (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_lab_shipyard = {
		-- id
		name = "Shipyard",
		description = "Produces Ships",
		side = "CORE",
		unitname = "core_t1_lab_shipyard",
		buildoptions = Shared.buildListCoreShipyard,
		objectname = "CORE_T1_LAB_Shipyard.s3o",
		buildpic = "CORE_T1_LAB_Shipyard.png",
		script = "CORE_T1_LAB_Shipyard.lua",
		corpse = "CORE_T1_LAB_Shipyard_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 750,  -- TA 3.1c (was 910)
		buildcostmetal = 600,  -- TA 3.1c (was 880)
		buildtime = 6000,  -- TA 3.1c (was 5100)
		energystorage = 100,
		metalstorage = 100,
		metalmake = 0.5,  -- TA 3.1c (was unset)
		-- movement or placement
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		minwaterdepth = 20,  -- 30
		-- nanolathing
		builder = 1,
		workertime = 100,  -- TA 3.1c (was 140)
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 2490,  -- TA 3.1c (was 2290)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 213,  -- TA 3.1c (was 367)
		-- unit animation
		waterline = 32,
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
