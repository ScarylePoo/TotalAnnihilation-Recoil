-- CORE_T2_DEF_Buzzsaw (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_buzzsaw = {
		-- id
		name = "Buzzsaw",
		description = "Rapid Fire Plasma Cannon",
		side = "CORE",
		unitname = "core_t2_def_buzzsaw",
		objectname = "CORE_T2_DEF_Buzzsaw",
		corpse = "CORE_T2_DEF_Buzzsaw_dead",
		icontype = "turret",
		category = "CORE LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 462648,
		buildcostmetal = 31564,
		buildtime = 365011,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "ATOMIC_BLAST",
		canattack = 1,
		canguard = 1,
		canstop = 1,
		firestandorders = 1,
		standingfireorder = 2,
		defaultmissiontype = "GUARD_NOMOVE",
		-- properties
		maxdamage = 1700,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 1,
		shootme = 1,
		buildangle = 29096,
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
				"servlrg4",
			},
			select = {
				"servlrg4",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "BUZZSAW",
				onlytargetcategory = "NOTAIR",
			},
		},
	},
}
