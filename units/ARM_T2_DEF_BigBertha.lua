-- ARM_T2_DEF_BigBertha (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_bigbertha = {
		-- id
		name = "Big Bertha",
		description = "Long Range Plasma Cannon",
		side = "ARM",
		unitname = "arm_t2_def_bigbertha",
		objectname = "ARM_T2_DEF_BigBertha.s3o",
		script = "ARM_T2_DEF_BigBertha.lua",
		corpse = "ARM_T2_DEF_BigBertha_dead",
		icontype = "turret",
		category = "ARM LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 124680,
		buildcostmetal = 6184,
		buildtime = 65185,
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
		maxdamage = 1800,
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
		noautofire = 0,
		shootme = 1,
		buildangle = 4096,
		ovradjust = 1,
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
				name = "BIG_BERTHA",
				onlytargetcategory = "NOTAIR",
			},
		},
	},
}
