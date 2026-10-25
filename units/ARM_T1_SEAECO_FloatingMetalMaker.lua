-- ARM_T1_SEAECO_FloatingMetalMaker (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seaeco_floatingmetalmaker = {
		-- id
		name = "Floating Metal Maker",
		description = "Converts Energy into Metal",
		side = "ARM",
		unitname = "arm_t1_seaeco_floatingmetalmaker",
		objectname = "ARM_T1_SEAECO_FloatingMetalMaker",
		script = "ARM_T1_SEAECO_FloatingMetalMaker.lua",
		corpse = "ARM_T1_SEAECO_FloatingMetalMaker_dead",
		icontype = "building",
		category = "ARM LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1480,
		buildtime = 2958,
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
		maxdamage = 110,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		waterline = 4,
		footprintx = 3,
		footprintz = 3,
		yardmap = "oooo oooo o",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		noshadow = 1,
		buildangle = 8192,
		sounds = {
			activate = "metlon1",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "metloff1",
			select = {
				"metlon1",
			},
			underattack = "warning1",
			working = "metlrun1",
		},
	},
}
