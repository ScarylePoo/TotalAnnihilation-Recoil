-- CORE_T1_DEF_Pulverizer (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_def_pulverizer = {
		-- id
		name = "Pulverizer",
		description = "Missile Tower",
		side = "CORE",
		unitname = "core_t1_def_pulverizer",
		objectname = "CORE_T1_DEF_Pulverizer.s3o",
		script = "CORE_T1_DEF_Pulverizer.lua",
		corpse = "CORE_T1_DEF_Pulverizer_dead",
		icontype = "turret",
		category = "CORE SPECIAL LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 805,
		buildcostmetal = 107,
		buildtime = 1749,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 20,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 450,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
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
		defaultmissiontype = "GUARD_NOMOVE",
		ovradjust = 1,
		sounds = {
			arrived = {
				"kbcorstp",
			},
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
				"kbcormov",
			},
			select = {
				"kbcorsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORRL_MISSILE",
			},
		},
	},
}
