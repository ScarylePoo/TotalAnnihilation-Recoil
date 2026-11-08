-- CORE_T1_SEADEF_Stinger (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seadef_stinger = {
		-- id
		name = "Stinger",
		description = "Missile Tower - Naval Series",
		side = "CORE",
		unitname = "core_t1_seadef_stinger",
		objectname = "CORE_T1_SEADEF_Stinger.s3o",
		buildpic = "CORE_T1_SEADEF_Stinger.png",
		script = "CORE_T1_SEADEF_Stinger.lua",
		corpse = "CORE_T1_SEADEF_Stinger_dead",
		icontype = "turret",
		category = "CORE SPECIAL LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1054,
		buildcostmetal = 72,
		buildtime = 2357,
		energyuse = 0.1,  -- TA 3.1c (was unset)
		-- movement or placement
		minwaterdepth = 2,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 290,  -- TA 3.1c (was 390)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
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
