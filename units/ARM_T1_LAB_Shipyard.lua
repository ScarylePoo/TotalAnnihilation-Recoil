-- ARM_T1_LAB_Shipyard (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_lab_shipyard = {
		-- id
		name = "Shipyard",
		description = "Produces Ships",
		side = "ARM",
		unitname = "arm_t1_lab_shipyard",
		buildoptions = Shared.buildListArmShipyard,
		objectname = "ARM_T1_LAB_Shipyard",
		corpse = "ARM_T1_LAB_Shipyard_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 805,
		buildcostmetal = 875,
		buildtime = 5050,
		energystorage = 100,
		metalstorage = 100,
		-- movement or placement
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		minwaterdepth = 20,  -- 30
		-- nanolathing
		builder = 1,
		workertime = 140,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 2290,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 365,
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
