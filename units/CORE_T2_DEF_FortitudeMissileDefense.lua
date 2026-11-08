-- CORE_T2_DEF_FortitudeMissileDefense (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_fortitudemissiledefense = {
		-- id
		name = "Fortitude Missile Defense",
		description = "Anti Missile Defense System",
		side = "CORE",
		unitname = "core_t2_def_fortitudemissiledefense",
		objectname = "CORE_T2_DEF_FortitudeMissileDefense.s3o",
		buildpic = "CORE_T2_DEF_FortitudeMissileDefense.png",
		script = "CORE_T2_DEF_FortitudeMissileDefense.lua",
		corpse = "CORE_T2_DEF_FortitudeMissileDefense_dead",
		category = "CORE SPECIAL LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 92321,
		buildcostmetal = 1508,  -- TA 3.1c (was 1708)
		buildtime = 96450,  -- TA 3.1c (was 56450)
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL NOTAIR",
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "CRAWL_BLASTSML",
		-- properties
		maxdamage = 780,  -- TA 3.1c (was 1180)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 150,  -- TA 3.1c (was 162)
		-- other abilities
		damagemodifier = 0.5,  -- TA 3.1c (was 0.4)
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 1,
		shootme = 1,
		buildangle = 4096,
		antiweapons = 1,
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
				"loadwtr1",
			},
			select = {
				"loadwtr1",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ANTI_NUCLEAR_MISSILE",
			},
		},
	},
}
