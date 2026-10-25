-- ARM_T2_DEF_Flakker (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_flakker = {
		-- id
		name = "Flakker",
		description = "Anti-Air Flak Gun",
		side = "ARM",
		unitname = "arm_t2_def_flakker",
		objectname = "ARM_T2_DEF_Flakker",
		script = "ARM_T2_DEF_Flakker.lua",
		corpse = "ARM_T2_DEF_Flakker_dead",
		icontype = "turret",
		category = "ARM LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 17425,
		buildcostmetal = 1069,
		buildtime = 20380,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "MEDIUM_BUILDING",
		-- properties
		maxdamage = 1524,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 610,
		-- unit animation
		footprintx = 2,
		footprintz = 2,
		yardmap = "oooo",  -- ooooooooo
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
		defaultmissiontype = "GUARD_NOMOVE",
		buildangle = 8192,
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
				"twrturn3",
			},
			select = {
				"twrturn3",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARMFLAK_GUN",
				onlytargetcategory = "VTOL",
			},
		},
	},
}
