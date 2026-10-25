-- ARM_T2_AIR_Phoenix (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_air_phoenix = {
		-- id
		name = "Phoenix",
		description = "Strategic Bomber",
		side = "ARM",
		unitname = "arm_t2_air_phoenix",
		objectname = "ARM_T2_AIR_Phoenix",
		corpse = "ARM_T2_AIR_Phoenix_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL2 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7624,
		buildcostmetal = 209,
		buildtime = 16064,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 220,
		maxvelocity = 10,
		brakerate = 4,
		acceleration = 0.06,
		turnrate = 365,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		nochasecategory = "UNDERWATER",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 470,
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
		attackrunlength = 180,
		altfromsealevel = 1,
		ovradjust = 1,
		sounds = {
			arrived = {
				"vtolarld",
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
				"vtolarmv",
			},
			select = {
				"vtolarac",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_PHOENIX_BOMB",
				onlytargetcategory = "NOTAIR",
			},
			{
				name = "ARM_PHOENIX_LASER",
				onlytargetcategory = "VTOL",
			},
		},
	},
}
