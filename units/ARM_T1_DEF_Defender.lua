-- ARM_T1_DEF_Defender (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_def_defender = {
		-- id
		name = "Defender",
		description = "Missile Tower",
		side = "ARM",
		unitname = "arm_t1_def_defender",
		objectname = "ARM_T1_DEF_Defender.s3o",
		script = "ARM_T1_DEF_Defender.lua",
		corpse = "ARM_T1_DEF_Defender_dead",
		icontype = "turret",
		category = "ARM SPECIAL LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 843,
		buildcostmetal = 116,
		buildtime = 1843,
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
		sightdistance = 600,
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
				"kbarmstp",
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
				"kbarmmov",
			},
			select = {
				"kbarmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARMRL_MISSILE",
			},
		},
	},
}
