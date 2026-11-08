-- ARM_T2_DEF_AdvancedRadar (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_advancedradar = {
		-- id
		name = "Advanced Radar Tower",
		description = "Long Range Radar Tower",
		side = "ARM",
		unitname = "arm_t2_def_advancedradar",
		objectname = "ARM_T2_DEF_AdvancedRadar.s3o",
		buildpic = "ARM_T2_DEF_AdvancedRadar.png",
		script = "ARM_T2_DEF_AdvancedRadar.lua",
		corpse = "ARM_T2_DEF_AdvancedRadar_dead",
		category = "ARM SPECIAL LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1830,
		buildcostmetal = 125,
		buildtime = 4800,
		energyuse = 18,
		energymake = 18,  -- TA 3.1c (was unset)
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 120,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 350,  -- TA 3.1c (was 550)
		radardistance = 2880,  -- TA 3.1c (was 3580)
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		smoothanim = 1,
		footprintx = 2,
		footprintz = 2,
		yardmap = "oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
		ovradjust = 1,
		sounds = {
			activate = "radadvn1",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "radadde1",
			select = {
				"radadvn1",
			},
			underattack = "warning1",
			working = "radar2",
		},
	},
}
