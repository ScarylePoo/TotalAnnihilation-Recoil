-- ARM_T1_SEAECO_TidalGenerator (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seaeco_tidalgenerator = {
		-- id
		name = "Tidal Generator",
		description = "Produces Energy",
		side = "ARM",
		unitname = "arm_t1_seaeco_tidalgenerator",
		objectname = "ARM_T1_SEAECO_TidalGenerator",
		script = "ARM_T1_SEAECO_TidalGenerator.lua",
		corpse = "ARM_T1_SEAECO_TidalGenerator_dead",
		icontype = "building",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 468,
		buildcostmetal = 82,
		buildtime = 2188,
		tidalgenerator = 1,
		-- movement or placement
		minwaterdepth = 20,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 256,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 175,
		-- unit animation
		waterline = 16,
		footprintx = 3,
		footprintz = 3,
		yardmap = "WWW WWW WWW",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
		noshadow = 1,
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
				"tidegen1",
			},
			underattack = "warning1",
		},
	},
}
