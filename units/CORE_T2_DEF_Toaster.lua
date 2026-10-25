-- CORE_T2_DEF_Toaster (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_toaster = {
		-- id
		name = "Toaster",
		description = "Pop-up Heavy Cannon",
		side = "CORE",
		unitname = "core_t2_def_toaster",
		objectname = "CORE_T2_DEF_Toaster",
		corpse = "CORE_T2_DEF_Toaster_dead",
		icontype = "turret",
		category = "CORE LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 12687,
		buildcostmetal = 2146,
		buildtime = 18377,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 1877,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 647,
		-- other abilities
		damagemodifier = 0.15,
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
				name = "CORTOAST_GUN",
				onlytargetcategory = "NOTAIR",
			},
		},
	},
}
