-- ARM_T1_SEAECO_UWEnergyStorage (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seaeco_uwenergystorage = {
		-- id
		name = "Underwater Energy Storage",
		description = "Increases Energy Storage by 4000",
		side = "ARM",
		unitname = "arm_t1_seaeco_uwenergystorage",
		objectname = "ARM_T1_SEAECO_UWEnergyStorage",
		script = "ARM_T1_SEAECO_UWEnergyStorage.lua",
		corpse = "ARM_T1_SEAECO_UWEnergyStorage_dead",
		icontype = "building",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2950,
		buildcostmetal = 284,
		buildtime = 15741,
		energystorage = 4000,
		-- movement or placement
		minwaterdepth = 30,
		maxslope = 20,
		-- combat
		explodeas = "ESTOR_BUILDINGEX",
		selfdestructas = "ESTOR_BUILDING",
		-- properties
		maxdamage = 1447,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 245,
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
				"storngy1",
			},
			underattack = "warning1",
		},
	},
}
