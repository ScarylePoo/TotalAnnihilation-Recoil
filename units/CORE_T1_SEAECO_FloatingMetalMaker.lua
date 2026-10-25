-- CORE_T1_SEAECO_FloatingMetalMaker (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seaeco_floatingmetalmaker = {
		-- id
		name = "Floating Metal Maker",
		description = "Converts Energy into Metal",
		side = "CORE",
		unitname = "core_t1_seaeco_floatingmetalmaker",
		objectname = "CORE_T1_SEAECO_FloatingMetalMaker",
		corpse = "CORE_T1_SEAECO_FloatingMetalMaker_dead",
		icontype = "building",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1530,
		buildtime = 2682,
		makesmetal = 1,
		energyuse = 60,
		-- movement or placement
		maxwaterdepth = 0,
		minwaterdepth = 11,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 120,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 365,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		waterline = 33,
		footprintx = 3,
		footprintz = 3,
		yardmap = "oooo oooo o",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
		sounds = {
			activate = "metlon2",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "metloff2",
			select = {
				"metlon2",
			},
			underattack = "warning1",
			working = "metlrun2",
		},
	},
}
