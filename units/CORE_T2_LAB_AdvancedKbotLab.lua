-- CORE_T2_LAB_AdvancedKbotLab (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_lab_advancedkbotlab = {
		-- id
		name = "Adv. Kbot Lab",
		description = "Produces Advanced Kbots",
		side = "CORE",
		unitname = "core_t2_lab_advancedkbotlab",
		buildoptions = Shared.buildListCoreAdvancedKbotLab,
		objectname = "CORE_T2_LAB_AdvancedKbotLab.s3o",
		buildpic = "CORE_T2_LAB_AdvancedKbotLab.png",
		script = "CORE_T2_LAB_AdvancedKbotLab.lua",
		corpse = "CORE_T2_LAB_AdvancedKbotLab_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3625,  -- TA 3.1c (was 9625)
		buildcostmetal = 1972,  -- TA 3.1c (was 2072)
		buildtime = 14000,  -- TA 3.1c (was 18212)
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
		workertime = 200,  -- TA 3.1c (was 260)
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 3170,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 222,  -- TA 3.1c (was 388)
		-- unit animation
		footprintx = 7,
		footprintz = 6,
		yardmap = "ooooooo ooooooo occccco ccccccc ccccccc oocccoo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 1024,
		ovradjust = 1,
		sounds = {
			build = "plabwork",
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
				"plabactv",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
