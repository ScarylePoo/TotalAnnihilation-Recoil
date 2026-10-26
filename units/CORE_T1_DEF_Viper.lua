-- CORE_T1_DEF_Viper (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_def_viper = {
		-- id
		name = "Viper",
		description = "Pop-Up Heavy Laser",
		side = "CORE",
		unitname = "core_t1_def_viper",
		objectname = "CORE_T1_DEF_Viper.s3o",
		corpse = "CORE_T1_DEF_Viper_dead",
		icontype = "turret",
		category = "CORE LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7787,
		buildcostmetal = 872,
		buildtime = 13528,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "MEDIUM_BUILDINGEX",
		selfdestructas = "MEDIUM_BUILDING",
		-- properties
		maxdamage = 1088,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 542,
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
				name = "CORE_HEAVY_LASER",
			},
		},
	},
}
