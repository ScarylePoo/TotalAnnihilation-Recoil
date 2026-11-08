-- ARM_T2_AIR_Hawk (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_air_hawk = {
		-- id
		name = "Hawk",
		description = "Stealth Fighter",
		side = "ARM",
		unitname = "arm_t2_air_hawk",
		objectname = "ARM_T2_AIR_Hawk.s3o",
		buildpic = "ARM_T2_AIR_Hawk.png",
		script = "ARM_T2_AIR_Hawk.lua",
		corpse = "ARM_T2_AIR_Hawk_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL2 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 6893,
		buildcostmetal = 254,
		buildtime = 15285,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 160,
		maxvelocity = 12,  -- TA 3.1c (was 17)
		brakerate = 9,  -- TA 3.1c (was 10)
		acceleration = 0.45,  -- TA 3.1c (was 0.85)
		turnrate = 820,  -- TA 3.1c (was 950)
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 510,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 350,
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
				name = "ARMVTOL_ADVMISSILE",
			},
			{
				name = "ARMVTOL_ADVMISSILE2",
			},
		},
	},
}
