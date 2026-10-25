-- ARM_T1_LAB_AircraftPlant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_lab_aircraftplant = {
		-- id
		name = "Aircraft Plant",
		description = "Produces Aircraft",
		side = "ARM",
		unitname = "arm_t1_lab_aircraftplant",
		buildoptions = Shared.buildListArmAircraftPlant,
		objectname = "ARM_T1_LAB_AircraftPlant",
		corpse = "ARM_T1_LAB_AircraftPlant_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1370,
		buildcostmetal = 850,
		buildtime = 7240,
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
		workertime = 110,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 1850,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 393,
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
