-- CORE_T2_AIR_Hurricane (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_air_hurricane = {
		-- id
		name = "Hurricane",
		description = "Strategic Bomber",
		side = "CORE",
		unitname = "core_t2_air_hurricane",
		objectname = "CORE_T2_AIR_Hurricane",
		corpse = "CORE_T2_AIR_Hurricane_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL2 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 8050,
		buildcostmetal = 220,
		buildtime = 16269,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 220,
		maxvelocity = 10.1,
		brakerate = 0.5,
		acceleration = 0.05,
		turnrate = 256,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		nochasecategory = "UNDERWATER",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 480,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		-- other abilities
		candropflare = 1,
		flarereload = 4,
		flareefficieny = 0.3,
		flaredelay = 0.3,
		flaredropvector = "0 -.4 -1.3",
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
		attackrunlength = 290,
		altfromsealevel = 1,
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
				name = "CORE_HURRICANE_BOMB",
				onlytargetcategory = "NOTAIR",
			},
			{
				name = "CORE_HURRICANE_LASER",
				onlytargetcategory = "VTOL",
			},
		},
	},
}
