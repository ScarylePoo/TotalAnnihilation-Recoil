-- CORE_T1_DEF_RadarTower (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_def_radartower = {
		-- id
		name = "Radar Tower",
		description = "Radar Tower",
		side = "CORE",
		unitname = "core_t1_def_radartower",
		objectname = "CORE_T1_DEF_RadarTower.s3o",
		corpse = "CORE_T1_DEF_RadarTower_dead",
		icontype = "building_radar_sonar",
		category = "CORE SPECIAL LEVEL1 NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 800,
		buildcostmetal = 50,
		buildtime = 1137,
		energyuse = 6,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 51,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		radardistance = 1740,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		footprintx = 2,
		footprintz = 2,
		yardmap = "oo oo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
		buildangle = 16384,
		ovradjust = 1,
		sounds = {
			activate = "radar1",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "radarde1",
			select = {
				"radar2",
			},
			underattack = "warning1",
			working = "radar2",
		},
	},
}
