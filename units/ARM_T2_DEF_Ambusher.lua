-- ARM_T2_DEF_Ambusher (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_ambusher = {
		-- id
		name = "Ambusher",
		description = "Pop-up Heavy Cannon",
		side = "ARM",
		unitname = "arm_t2_def_ambusher",
		objectname = "ARM_T2_DEF_Ambusher",
		corpse = "ARM_T2_DEF_Ambusher_dead",
		icontype = "turret",
		category = "ARM LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 16821,
		buildcostmetal = 2002,
		buildtime = 20172,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		explodeas = "lARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 1658,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 630,
		-- other abilities
		damagemodifier = 0.28,
		-- unit animation
		footprintx = 3,
		footprintz = 3,
		yardmap = "oooo oooo o",
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
				"twrturn3",
			},
			select = {
				"twrturn3",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARMAMB_GUN",
				onlytargetcategory = "NOTAIR",
			},
		},
	},
}
