-- CORE_T2_DEF_Silencer (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_silencer = {
		-- id
		name = "Silencer",
		description = "Nuclear Missile Launcher",
		side = "CORE",
		unitname = "core_t2_def_silencer",
		objectname = "CORE_T2_DEF_Silencer.s3o",
		corpse = "CORE_T2_DEF_Silencer_dead",
		icontype = "nuke",
		category = "CORE SPECIAL LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 136068,
		buildcostmetal = 3075,
		buildtime = 121243,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "ATOMIC_BLASTEX",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 3160,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 350,
		-- unit animation
		footprintx = 6,
		footprintz = 7,
		yardmap = "oooooo oooooo oooooo oooooo oooooo oooooo oooooo",
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
