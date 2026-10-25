-- CORE_T2_DEF_FortitudeMissileDefense (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_fortitudemissiledefense = {
		-- id
		name = "Fortitude Missile Defense",
		description = "Anti Missile Defense System",
		side = "CORE",
		unitname = "core_t2_def_fortitudemissiledefense",
		objectname = "CORE_T2_DEF_FortitudeMissileDefense",
		corpse = "CORE_T2_DEF_FortitudeMissileDefense_dead",
		icontype = "nuke",
		category = "CORE SPECIAL LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 92321,
		buildcostmetal = 1708,
		buildtime = 56450,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL NOTAIR",
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "CRAWL_BLASTEX",
		-- properties
		maxdamage = 1180,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 162,
		-- other abilities
		damagemodifier = 0.4,
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
