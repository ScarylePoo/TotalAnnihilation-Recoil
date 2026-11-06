-- CORE_T2_SEADEF_AdvancedSonar (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_seadef_advancedsonar = {
		-- id
		name = "Advanced Sonar Station",
		description = "Locates Water Units",
		side = "CORE",
		unitname = "core_t2_seadef_advancedsonar",
		objectname = "CORE_T2_SEADEF_AdvancedSonar.s3o",
		buildpic = "CORE_T2_SEADEF_AdvancedSonar.png",
		script = "CORE_T2_SEADEF_AdvancedSonar.lua",
		corpse = "CORE_T2_SEADEF_AdvancedSonar_dead",
		icontype = "building_radar_sonar",
		category = "CORE SPECIAL LEVEL2 NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2257,
		buildcostmetal = 152,
		buildtime = 6096,
		energyuse = 18,
		energymake = 18,  -- TA 3.1c (was unset)
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
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 210,  -- TA 3.1c (was 367)
		sonardistance = 2250,  -- TA 3.1c (was 2650)
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
