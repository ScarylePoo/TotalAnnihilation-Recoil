-- CORE_T1_DEF_GaatGun (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_def_gaatgun = {
		-- id
		name = "Gaat Gun",
		description = "Heavy Laser Tower",
		side = "CORE",
		unitname = "core_t1_def_gaatgun",
		objectname = "CORE_T1_DEF_GaatGun.s3o",
		corpse = "CORE_T1_DEF_GaatGun_dead",
		icontype = "turret",
		category = "CORE LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5443,
		buildcostmetal = 589,
		buildtime = 9622,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "MEDIUM_BUILDINGEX",
		selfdestructas = "MEDIUM_BUILDING",
		-- properties
		maxdamage = 1000,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 613,
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
		buildangle = 4096,
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
				"twractv3",
			},
			select = {
				"twractv3",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORE_HEAVY_LASER",
			},
		},
	},
}
