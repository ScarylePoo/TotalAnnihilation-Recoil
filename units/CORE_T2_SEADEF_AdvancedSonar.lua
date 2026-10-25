-- CORE_T2_SEADEF_AdvancedSonar (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_seadef_advancedsonar = {
		-- id
		name = "Advanced Sonar Station",
		description = "Locates Water Units",
		side = "CORE",
		unitname = "core_t2_seadef_advancedsonar",
		objectname = "CORE_T2_SEADEF_AdvancedSonar",
		corpse = "CORE_T2_SEADEF_AdvancedSonar_dead",
		icontype = "building_radar_sonar",
		category = "CORE SPECIAL LEVEL2 NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2257,
		buildcostmetal = 152,
		buildtime = 6096,
		energyuse = 18,
		-- movement or placement
		minwaterdepth = 24,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 240,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		sonardistance = 2650,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		waterline = 0,
		footprintx = 3,
		footprintz = 3,
		yardmap = "oooo oooo o",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
		noshadow = 1,
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
			deactivate = "sonarde2",
			select = {
				"sonar2",
			},
			underattack = "warning1",
		},
	},
}
