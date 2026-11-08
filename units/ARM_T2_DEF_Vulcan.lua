-- ARM_T2_DEF_Vulcan (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_vulcan = {
		-- id
		name = "Vulcan",
		description = "Rapid Fire Plasma Cannon",
		side = "ARM",
		unitname = "arm_t2_def_vulcan",
		objectname = "ARM_T2_DEF_Vulcan.s3o",
		buildpic = "ARM_T2_DEF_Vulcan.png",
		script = "ARM_T2_DEF_Vulcan.lua",
		corpse = "ARM_T2_DEF_Vulcan_dead",
		icontype = "turret",
		category = "ARM LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 479111,
		buildcostmetal = 45198,  -- TA 3.1c (was 30198)
		buildtime = 587421,  -- TA 3.1c (was 325421)
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
		maxdamage = 1400,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 210,  -- TA 3.1c (was 367)
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
				"servlrg3",
			},
			select = {
				"servlrg3",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "VULCAN",
				onlytargetcategory = "NOTAIR",
			},
		},
	},
}
