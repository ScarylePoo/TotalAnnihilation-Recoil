-- ARM_T2_DEF_Retaliator (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_retaliator = {
		-- id
		name = "Retaliator",
		description = "Nuclear Missile Launcher",
		side = "ARM",
		unitname = "arm_t2_def_retaliator",
		objectname = "ARM_T2_DEF_Retaliator",
		corpse = "ARM_T2_DEF_Retaliator_dead",
		icontype = "nuke",
		category = "ARM SPECIAL LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 140134,
		buildcostmetal = 3010,
		buildtime = 118453,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "ATOMIC_BLASTEX",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 3079,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 350,
		-- unit animation
		footprintx = 5,
		footprintz = 5,
		yardmap = "oooo oooo oooo oooo oooo oooo o",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
		buildangle = 8192,
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
				"servroc1",
			},
			select = {
				"servroc1",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "NUCLEAR_MISSILE",
			},
		},
	},
}
