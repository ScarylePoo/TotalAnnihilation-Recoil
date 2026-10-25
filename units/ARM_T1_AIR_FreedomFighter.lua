-- ARM_T1_AIR_FreedomFighter (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_air_freedomfighter = {
		-- id
		name = "Freedom Fighter",
		description = "Fighter",
		side = "ARM",
		unitname = "arm_t1_air_freedomfighter",
		objectname = "ARM_T1_AIR_FreedomFighter",
		corpse = "ARM_T1_AIR_FreedomFighter_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL1 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3234,
		buildcostmetal = 110,
		buildtime = 9182,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 110,
		maxvelocity = 16,
		brakerate = 6,
		acceleration = 0.55,
		turnrate = 750,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 196,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 610,
		-- other abilities
		canloopbackattack = 1,
		-- unit animation
		collide = 0,
		footprintx = 2,
		footprintz = 2,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		bankscale = 1,
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
				name = "ARMVTOL_MISSILE",
			},
		},
	},
}
