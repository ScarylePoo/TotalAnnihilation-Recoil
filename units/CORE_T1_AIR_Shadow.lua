-- CORE_T1_AIR_Shadow (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_air_shadow = {
		-- id
		name = "Shadow",
		description = "Bomber",
		side = "CORE",
		unitname = "core_t1_air_shadow",
		objectname = "CORE_T1_AIR_Shadow",
		corpse = "CORE_T1_AIR_Shadow_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL1 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5691,
		buildcostmetal = 131,
		buildtime = 10750,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 205,
		maxvelocity = 9,
		brakerate = 1.2,
		acceleration = 0.07,
		turnrate = 335,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		nochasecategory = "UNDERWATER",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 315,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 522,
		-- unit animation
		collide = 0,
		footprintx = 3,
		footprintz = 3,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "VTOL_standby",
		maneuverleashlength = 1280,
		altfromsealevel = 1,
		attackrunlength = 220,
		ovradjust = 1,
		sounds = {
			arrived = {
				"vtolcrld",
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
				"vtolcrmv",
			},
			select = {
				"vtolcrac",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORE_SHADOW_BOMB",
			},
		},
	},
}
