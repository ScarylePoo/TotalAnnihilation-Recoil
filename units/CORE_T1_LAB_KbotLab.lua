-- CORE_T1_LAB_KbotLab (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_lab_kbotlab = {
		-- id
		name = "Kbot Lab",
		description = "Produces Kbots",
		side = "CORE",
		unitname = "core_t1_lab_kbotlab",
		buildoptions = Shared.buildListCoreKbotLab,
		objectname = "CORE_T1_LAB_KbotLab",
		corpse = "CORE_T1_LAB_KbotLab_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 650,
		buildcostmetal = 680,
		buildtime = 6106,
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
		workertime = 130,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 2600,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 387,
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
