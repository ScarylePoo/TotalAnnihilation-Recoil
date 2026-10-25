-- ARM_T1_SEADEF_SonarStation (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seadef_sonarstation = {
		-- id
		name = "Sonar Station",
		description = "Locates Water Units",
		side = "ARM",
		unitname = "arm_t1_seadef_sonarstation",
		objectname = "ARM_T1_SEADEF_SonarStation",
		script = "ARM_T1_SEADEF_SonarStation.lua",
		corpse = "ARM_T1_SEADEF_SonarStation_dead",
		icontype = "building_radar_sonar",
		category = "ARM SPECIAL LEVEL1 NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 403,
		buildcostmetal = 20,
		buildtime = 912,
		energyuse = 9,
		-- movement or placement
		maxslope = 10,
		minwaterdepth = 8,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 50,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 306,
		sonardistance = 1580,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		waterline = 33,
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
			deactivate = "sonarde1",
			select = {
				"sonar1",
			},
			underattack = "warning1",
		},
	},
}
