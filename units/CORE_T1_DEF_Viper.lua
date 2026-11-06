-- CORE_T1_DEF_Viper (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_def_viper = {
		-- id
		name = "Viper",
		description = "Pop-Up Heavy Laser",
		side = "CORE",
		unitname = "core_t1_def_viper",
		objectname = "CORE_T1_DEF_Viper.s3o",
		buildpic = "CORE_T1_DEF_Viper.png",
		script = "CORE_T1_DEF_Viper.lua",
		corpse = "CORE_T1_DEF_Viper_dead",
		icontype = "turret",
		category = "CORE LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 6687,  -- TA 3.1c (was 7787)
		buildcostmetal = 642,  -- TA 3.1c (was 872)
		buildtime = 11528,  -- TA 3.1c (was 13528)
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "MEDIUM_BUILDINGEX",
		selfdestructas = "MEDIUM_BUILDING",
		-- properties
		maxdamage = 988,  -- TA 3.1c (was 1088)
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 310,  -- TA 3.1c (was 542)
		-- other abilities
		damagemodifier = 0.125,
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
		defaultmissiontype = "GUARD_NOMOVE",
		buildangle = 8192,
		digger = 1,
		sounds = {
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			ok = {
				"servmed1",
			},
			select = {
				"servmed1",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORVIPE_LASER",
			},
		},
	},
}
