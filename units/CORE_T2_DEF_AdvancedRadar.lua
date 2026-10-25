-- CORE_T2_DEF_AdvancedRadar (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_advancedradar = {
		-- id
		name = "Advanced Radar Tower",
		description = "Long Range Radar",
		side = "CORE",
		unitname = "core_t2_def_advancedradar",
		objectname = "CORE_T2_DEF_AdvancedRadar",
		corpse = "CORE_T2_DEF_AdvancedRadar_dead",
		icontype = "building_radar_sonar",
		category = "CORE SPECIAL LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1920,
		buildcostmetal = 122,
		buildtime = 4960,
		energyuse = 17,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 130,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		radardistance = 3580,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		smoothanim = 1,
		footprintx = 2,
		footprintz = 2,
		yardmap = "oo oo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
		ovradjust = 1,
		sounds = {
			activate = "radadvn2",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "radadde2",
			select = {
				"radadvn2",
			},
			underattack = "warning1",
			working = "radar2",
		},
	},
}
