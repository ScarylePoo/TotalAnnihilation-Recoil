-- CORE_T1_SEADEF_SonarStation (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seadef_sonarstation = {
		-- id
		name = "Sonar Station",
		description = "Sonar Station",
		side = "CORE",
		unitname = "core_t1_seadef_sonarstation",
		objectname = "CORE_T1_SEADEF_SonarStation",
		corpse = "CORE_T1_SEADEF_SonarStation_dead",
		icontype = "building_radar_sonar",
		category = "CORE SPECIAL LEVEL1 NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 399,
		buildcostmetal = 20,
		buildtime = 900,
		energyuse = 8,
		-- movement or placement
		minwaterdepth = 10,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 52,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 306,
		sonardistance = 1523,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		waterline = 37,
		footprintx = 2,
		footprintz = 2,
		yardmap = "wwww",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
		noshadow = 1,
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
			deactivate = "sonarde2",
			select = {
				"sonar2",
			},
			underattack = "warning1",
		},
	},
}
