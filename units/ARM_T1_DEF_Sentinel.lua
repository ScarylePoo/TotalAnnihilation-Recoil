-- ARM_T1_DEF_Sentinel (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_def_sentinel = {
		-- id
		name = "Sentinel",
		description = "Heavy Laser Tower",
		side = "ARM",
		unitname = "arm_t1_def_sentinel",
		objectname = "ARM_T1_DEF_Sentinel",
		script = "ARM_T1_DEF_Sentinel.lua",
		corpse = "ARM_T1_DEF_Sentinel_dead",
		icontype = "turret",
		category = "ARM LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5398,
		buildcostmetal = 584,
		buildtime = 9575,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "MEDIUM_BUILDINGEX",
		selfdestructas = "MEDIUM_BUILDING",
		-- properties
		maxdamage = 930,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 635,
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
				"twractv3",
			},
			select = {
				"twractv3",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_TOWER_HEAVY_LASER",
			},
		},
	},
}
