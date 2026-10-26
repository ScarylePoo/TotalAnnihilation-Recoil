-- CORE_T2_AIR_Rapier (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_air_rapier = {
		-- id
		name = "Rapier",
		description = "Gunship",
		side = "CORE",
		unitname = "core_t2_air_rapier",
		objectname = "CORE_T2_AIR_Rapier.s3o",
		corpse = "CORE_T2_AIR_Rapier_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL2 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5778,
		buildcostmetal = 294,
		buildtime = 13294,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 85,
		maxvelocity = 8.1,
		brakerate = 3,
		acceleration = 0.24,
		turnrate = 600,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		hoverattack = 1,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 940,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
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
				name = "VTOL_rocket",
			},
			{
				name = "VTOL_rocket2",
			},
		},
	},
}
