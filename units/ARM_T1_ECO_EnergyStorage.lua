-- ARM_T1_ECO_EnergyStorage (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_eco_energystorage = {
		-- id
		name = "Energy Storage",
		description = "Increases Energy Storage by 3000",
		side = "ARM",
		unitname = "arm_t1_eco_energystorage",
		objectname = "ARM_T1_ECO_EnergyStorage.s3o",
		script = "ARM_T1_ECO_EnergyStorage.lua",
		corpse = "ARM_T1_ECO_EnergyStorage_dead",
		icontype = "building",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1030,
		buildcostmetal = 240,
		buildtime = 8710,
		energystorage = 3000,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "CRAWL_BLASTEX",
		selfdestructas = "CRAWL_BLASTEX",
		-- properties
		maxdamage = 1000,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		buildangle = 4096,
		ovradjust = 1,
		sounds = {
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
				"storngy1",
			},
			underattack = "warning1",
		},
	},
}
