-- CORE_T1_ECO_EnergyStorage (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_eco_energystorage = {
		-- id
		name = "Energy Storage",
		description = "Increases Energy Storage by 3000",
		side = "CORE",
		unitname = "core_t1_eco_energystorage",
		objectname = "CORE_T1_ECO_EnergyStorage",
		corpse = "CORE_T1_ECO_EnergyStorage_dead",
		icontype = "building",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1090,
		buildcostmetal = 250,
		buildtime = 8750,
		energystorage = 3000,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "CRAWL_BLASTEX",
		selfdestructas = "CRAWL_BLASTEX",
		-- properties
		maxdamage = 1070,
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
		noautofire = 0,
		buildangle = 8196,
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
				"storngy2",
			},
			underattack = "warning1",
		},
	},
}
