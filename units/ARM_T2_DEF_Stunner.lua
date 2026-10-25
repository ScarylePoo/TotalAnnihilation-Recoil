-- ARM_T2_DEF_Stunner (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_stunner = {
		-- id
		name = "Stunner",
		description = "EMP Missile Launcher",
		side = "ARM",
		unitname = "arm_t2_def_stunner",
		objectname = "ARM_T2_DEF_Stunner",
		corpse = "ARM_T2_DEF_Stunner_dead",
		icontype = "nuke",
		category = "ARM SPECIAL LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 45134,
		buildcostmetal = 1038,
		buildtime = 85453,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "ATOMIC_BLASTEX",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 2300,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 156,
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
				name = "STUNNER_MISSILE",
			},
		},
	},
}
