-- ARM_T1_SEADEF_Defender (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seadef_defender = {
		-- id
		name = "Defender",
		description = "Missile Tower - Naval Series",
		side = "ARM",
		unitname = "arm_t1_seadef_defender",
		objectname = "ARM_T1_SEADEF_Defender",
		script = "ARM_T1_SEADEF_Defender.lua",
		corpse = "ARM_T1_SEADEF_Defender_dead",
		icontype = "turret",
		category = "ARM SPECIAL LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 987,
		buildcostmetal = 71,
		buildtime = 2163,
		-- movement or placement
		minwaterdepth = 2,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 252,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 600,
		-- unit animation
		waterline = 15,
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
		defaultmissiontype = "GUARD_NOMOVE",
		buildangle = 16384,
		noshadow = 1,
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
