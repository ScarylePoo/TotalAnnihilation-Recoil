-- CORE_T2_AIR_Vamp (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_air_vamp = {
		-- id
		name = "Vamp",
		description = "Stealth Fighter",
		side = "CORE",
		unitname = "core_t2_air_vamp",
		objectname = "CORE_T2_AIR_Vamp.s3o",
		corpse = "CORE_T2_AIR_Vamp_dead",
		icontype = "aircraft",
		category = "CORE VTOL LEVEL2 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 6973,
		buildcostmetal = 257,
		buildtime = 15924,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 160,
		maxvelocity = 17,
		brakerate = 7,
		acceleration = 0.85,
		turnrate = 920,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 490,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		-- other abilities
		canloopbackattack = 1,
		stealth = 1,
		candropflare = 1,
		flarereload = 3,
		flareefficieny = 0.3,
		flaredelay = 0.1,
		flaredropvector = "0 0 -1",
		-- unit animation
		collide = 0,
		footprintx = 2,
		footprintz = 2,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
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
				name = "CORE_STEALTH_FIGHTER_MISSILE",
			},
			{
				name = "CORE_STEALTH_FIGHTER_MISSILE",
			},
		},
	},
}
