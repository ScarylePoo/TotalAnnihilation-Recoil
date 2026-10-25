-- ARM_T1_LAB_KbotLab (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_lab_kbotlab = {
		-- id
		name = "Kbot Lab",
		description = "Produces Kbots",
		side = "ARM",
		unitname = "arm_t1_lab_kbotlab",
		buildoptions = Shared.buildListArmKbotLab,
		objectname = "ARM_T1_LAB_KbotLab",
		corpse = "ARM_T1_LAB_KbotLab_dead",
		icontype = "factory",
		category = "ARM PLANT LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 830,
		buildcostmetal = 685,
		buildtime = 5760,
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
		maxdamage = 2690,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 403,
		-- unit animation
		footprintx = 6,
		footprintz = 6,
		yardmap = "yoccoy ooccoo ooccoo ooccoo ooccoo yoccoy",
		-- what are these? or more importantly, do they work/have meaning?
		energyuse = 0,
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		scale = 0.75,
		buildangle = 4096,
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
