-- CORE_T1_SEADEF_Stinger (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seadef_stinger = {
		-- id
		name = "Stinger",
		description = "Missile Tower - Naval Series",
		side = "CORE",
		unitname = "core_t1_seadef_stinger",
		objectname = "CORE_T1_SEADEF_Stinger",
		script = "CORE_T1_SEADEF_Stinger.lua",
		corpse = "CORE_T1_SEADEF_Stinger_dead",
		icontype = "turret",
		category = "CORE SPECIAL LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1054,
		buildcostmetal = 72,
		buildtime = 2357,
		-- movement or placement
		minwaterdepth = 2,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 390,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 360,
		-- unit animation
		waterline = 20,
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
				name = "corfrt_missile",
			},
		},
	},
}
