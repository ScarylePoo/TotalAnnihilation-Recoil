-- ARM_T2_SEADEF_AdvancedSonar (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_seadef_advancedsonar = {
		-- id
		name = "Advanced Sonar Station",
		description = "Extended Sonar",
		side = "ARM",
		unitname = "arm_t2_seadef_advancedsonar",
		objectname = "ARM_T2_SEADEF_AdvancedSonar",
		script = "ARM_T2_SEADEF_AdvancedSonar.lua",
		corpse = "ARM_T2_SEADEF_AdvancedSonar_dead",
		icontype = "building_radar_sonar",
		category = "ARM SPECIAL LEVEL2 NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2469,
		buildcostmetal = 163,
		buildtime = 6152,
		energyuse = 22,
		-- movement or placement
		maxslope = 10,
		minwaterdepth = 24,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 320,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 323,
		sonardistance = 2650,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		damagemodifier = 0.46,
		-- unit animation
		waterline = 34,
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		workertime = 0,
		bmcode = 0,
		builder = 0,
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
			deactivate = "sonarde1",
			select = {
				"sonar1",
			},
			underattack = "warning1",
		},
	},
}
