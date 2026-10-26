-- ARM_T2_AIR_Seahawk (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_air_seahawk = {
		-- id
		name = "Seahawk",
		description = "Airborne Sonar",
		side = "ARM",
		unitname = "arm_t2_air_seahawk",
		objectname = "ARM_T2_AIR_Seahawk.s3o",
		corpse = "ARM_T2_AIR_Seahawk_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL2 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7624,
		buildcostmetal = 139,
		buildtime = 10064,
		energyuse = 12,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 220,
		maxvelocity = 9.5,
		brakerate = 4,
		acceleration = 0.06,
		turnrate = 365,
		maxwaterdepth = 255,
		maxslope = 10,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 540,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 612,
		sonardistance = 1505,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
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
		amphibious = 1,
		sounds = {
			arrived = {
				"vtolarld",
			},
			build = "nanlath1",
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
			repair = "repair1",
			select = {
				"seasonr2",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
