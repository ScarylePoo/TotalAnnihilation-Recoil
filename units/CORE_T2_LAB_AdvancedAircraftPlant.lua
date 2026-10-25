-- CORE_T2_LAB_AdvancedAircraftPlant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_lab_advancedaircraftplant = {
		-- id
		name = "Adv. Aircraft Plant",
		description = "Produces Advanced Aircraft",
		side = "CORE",
		unitname = "core_t2_lab_advancedaircraftplant",
		buildoptions = Shared.buildListCoreAdvancedAircraftPlant,
		objectname = "CORE_T2_LAB_AdvancedAircraftPlant",
		corpse = "CORE_T2_LAB_AdvancedAircraftPlant_dead",
		icontype = "factory",
		category = "CORE PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 15422,
		buildcostmetal = 2491,
		buildtime = 21232,
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
		workertime = 220,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 2200,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 411,
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
