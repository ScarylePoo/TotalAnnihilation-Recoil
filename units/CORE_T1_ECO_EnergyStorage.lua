-- CORE_T1_ECO_EnergyStorage (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_eco_energystorage = {
		-- id
		name = "Energy Storage",
		description = "Increases Energy Storage by 3000",
		side = "CORE",
		unitname = "core_t1_eco_energystorage",
		objectname = "CORE_T1_ECO_EnergyStorage.s3o",
		buildpic = "CORE_T1_ECO_EnergyStorage.png",
		script = "CORE_T1_ECO_EnergyStorage.lua",
		corpse = "CORE_T1_ECO_EnergyStorage_dead",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2490,  -- TA 3.1c (was 1090)
		buildcostmetal = 250,
		buildtime = 12750,  -- TA 3.1c (was 8750)
		energystorage = 3000,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "ESTOR_BUILDINGEX",
		selfdestructas = "ESTOR_BUILDING",
		-- properties
		maxdamage = 1070,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 210,  -- TA 3.1c (was 367)
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
