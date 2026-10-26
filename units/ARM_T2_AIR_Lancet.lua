-- ARM_T2_AIR_Lancet (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_air_lancet = {
		-- id
		name = "Lancet",
		description = "Torpedo Bomber",
		side = "ARM",
		unitname = "arm_t2_air_lancet",
		objectname = "ARM_T2_AIR_Lancet.s3o",
		corpse = "ARM_T2_AIR_Lancet_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL2 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 6438,
		buildcostmetal = 378,
		buildtime = 14096,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 150,
		maxvelocity = 9.7,
		brakerate = 6,
		acceleration = 0.2,
		turnrate = 420,
		maxwaterdepth = 255,
		maxslope = 10,
		-- combat
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 370,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 610,
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
				name = "ARMAIR_TORPEDO",
			},
		},
	},
}
