-- ARM_T2_AIR_Brawler (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_air_brawler = {
		-- id
		name = "Brawler",
		description = "Gunship",
		side = "ARM",
		unitname = "arm_t2_air_brawler",
		objectname = "ARM_T2_AIR_Brawler.s3o",
		corpse = "ARM_T2_AIR_Brawler_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL2 WEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 6249,
		buildcostmetal = 314,
		buildtime = 14385,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 100,
		maxvelocity = 6.6,
		brakerate = 4,
		acceleration = 0.16,
		turnrate = 800,
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
		maxdamage = 920,
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
				name = "VTOL_EMG",
			},
		},
	},
}
