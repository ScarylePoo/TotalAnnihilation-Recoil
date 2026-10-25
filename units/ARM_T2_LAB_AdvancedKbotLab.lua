-- ARM_T2_LAB_AdvancedKbotLab (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_lab_advancedkbotlab = {
		-- id
		name = "Adv. Kbot Lab",
		description = "Produces Advanced Kbots",
		side = "ARM",
		unitname = "arm_t2_lab_advancedkbotlab",
		buildoptions = Shared.buildListArmAdvancedKbotLab,
		objectname = "ARM_T2_LAB_AdvancedKbotLab",
		corpse = "ARM_T2_LAB_AdvancedKbotLab_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 9277,
		buildcostmetal = 2007,
		buildtime = 17520,
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
		workertime = 260,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 3005,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 385,
		-- unit animation
		footprintx = 5,
		footprintz = 6,
		yardmap = "occco occco occco occco occco occco",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 2048,
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
