-- ARM_T1_DEF_Mine4 (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_def_mine4 = {
		-- id
		name = "HE Area Mine",
		description = "Med. Damage, Large Range Mine",
		side = "ARM",
		unitname = "arm_t1_def_mine4",
		objectname = "ARM_T1_DEF_Mine4",
		script = "ARM_T1_DEF_Mine4.lua",
		category = "ARM MINE LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4294,
		buildcostmetal = 137,
		buildtime = 5582,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 15,
		-- combat
		firestate = 2,
		kamikaze = 1,
		kamikazedistance = 10,
		selfdestructcountdown = 1,
		explodeas = "ARMMINE4",
		selfdestructas = "ARMMINE4",
		-- properties
		maxdamage = 100,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 60,
		-- other abilities
		stealth = 1,
		cloakcost = 31,
		mincloakdistance = 10,
		-- unit animation
		footprintx = 1,
		footprintz = 1,
		yardmap = "o",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		defaultmissiontype = "Standby_Mine",
		initcloaked = 1,
		sounds = {
			arrived = {
				"servsml6",
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
				"servsml6",
			},
			select = {
				"minesel1",
			},
			underattack = "warning1",
		},
	},
}
