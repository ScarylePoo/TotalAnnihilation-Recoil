-- ARM_T1_DEF_LLT (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_def_llt = {
		-- id
		name = "L.L.T.",
		description = "Light Laser Tower",
		side = "ARM",
		unitname = "arm_t1_def_llt",
		objectname = "ARM_T1_DEF_LLT",
		script = "ARM_T1_DEF_LLT.lua",
		corpse = "ARM_T1_DEF_LLT_dead",
		icontype = "turret",
		category = "ARM LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1946,
		buildcostmetal = 190,
		buildtime = 4662,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 14,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "MEDIUM_BUILDINGEX",
		selfdestructas = "MEDIUM_BUILDING",
		-- properties
		maxdamage = 550,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 665,
		-- unit animation
		footprintx = 2,
		footprintz = 2,
		yardmap = "oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
		defaultmissiontype = "GUARD_NOMOVE",
		buildangle = 32768,
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
				"servmed2",
			},
			select = {
				"servmed2",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_TOWER_LIGHT_LASER",
			},
		},
	},
}
