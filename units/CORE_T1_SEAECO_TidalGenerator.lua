-- CORE_T1_SEAECO_TidalGenerator (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seaeco_tidalgenerator = {
		-- id
		name = "Tidal Generator",
		description = "Produces Energy",
		side = "CORE",
		unitname = "core_t1_seaeco_tidalgenerator",
		objectname = "CORE_T1_SEAECO_TidalGenerator.s3o",
		buildpic = "CORE_T1_SEAECO_TidalGenerator.png",
		script = "CORE_T1_SEAECO_TidalGenerator.lua",
		corpse = "CORE_T1_SEAECO_TidalGenerator_dead",
		icontype = "building",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 752,  -- TA 3.1c (was 452)
		buildcostmetal = 81,
		buildtime = 2094,
		tidalgenerator = 1,
		-- movement or placement
		minwaterdepth = 20,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 253,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 100,  -- TA 3.1c (was 175)
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		waterline = 20,
		footprintx = 4,
		footprintz = 4,
		yardmap = "wwww wwww wwww wwww",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 4096,
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
				"tidegen2",
			},
			underattack = "warning1",
		},
	},
}
