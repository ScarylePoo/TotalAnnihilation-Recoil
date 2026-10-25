-- CORE_T1_SEAECO_UWEnergyStorage (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seaeco_uwenergystorage = {
		-- id
		name = "Underwater Energy Storage",
		description = "Increases Energy Storage by 4000",
		side = "CORE",
		unitname = "core_t1_seaeco_uwenergystorage",
		objectname = "CORE_T1_SEAECO_UWEnergyStorage",
		corpse = "CORE_T1_SEAECO_UWEnergyStorage_dead",
		icontype = "building",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2540,
		buildcostmetal = 280,
		buildtime = 14482,
		energystorage = 4000,
		-- movement or placement
		minwaterdepth = 31,
		maxslope = 20,
		-- combat
		explodeas = "ESTOR_BUILDINGEX",
		selfdestructas = "ESTOR_BUILDING",
		-- properties
		maxdamage = 1521,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 227,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
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
