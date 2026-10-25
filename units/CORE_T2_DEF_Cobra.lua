-- CORE_T2_DEF_Cobra (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_cobra = {
		-- id
		name = "Cobra",
		description = "Anti-Air Flak Gun",
		side = "CORE",
		unitname = "core_t2_def_cobra",
		objectname = "CORE_T2_DEF_Cobra",
		corpse = "CORE_T2_DEF_Cobra_dead",
		icontype = "turret",
		category = "CORE LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 18995,
		buildcostmetal = 1092,
		buildtime = 21223,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "MEDIUM_BUILDING",
		-- properties
		maxdamage = 1655,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 595,
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
				name = "CORFLAK_GUN",
				onlytargetcategory = "VTOL",
			},
		},
	},
}
