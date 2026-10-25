-- CORE_T2_DEF_Intimidator (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_intimidator = {
		-- id
		name = "Intimidator",
		description = "Long Range Plasma Cannon",
		side = "CORE",
		unitname = "core_t2_def_intimidator",
		objectname = "CORE_T2_DEF_Intimidator",
		corpse = "CORE_T2_DEF_Intimidator_dead",
		icontype = "turret",
		category = "CORE LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 122520,
		buildcostmetal = 6328,
		buildtime = 73237,
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
		maxdamage = 1900,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- unit animation
		footprintx = 3,
		footprintz = 3,
		yardmap = "ooo ooo ooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
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
				"servlrg4",
			},
			select = {
				"servlrg4",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "INTIMIDATOR",
				onlytargetcategory = "NOTAIR",
			},
		},
	},
}
