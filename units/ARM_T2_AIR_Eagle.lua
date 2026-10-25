-- ARM_T2_AIR_Eagle (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_air_eagle = {
		-- id
		name = "Eagle",
		description = "Radar Plane",
		side = "ARM",
		unitname = "arm_t2_air_eagle",
		objectname = "ARM_T2_AIR_Eagle",
		corpse = "ARM_T2_AIR_Eagle_dead",
		icontype = "aircraft",
		category = "ARM VTOL LEVEL2 NOWEAPON NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 8062,
		buildcostmetal = 165,
		buildtime = 12819,
		energyuse = 23,
		-- movement or placement
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		canfly = 1,
		cruisealt = 160,
		maxvelocity = 9.2,
		brakerate = 4,
		acceleration = 0.11,
		turnrate = 356,
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 110,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 650,
		radardistance = 2250,
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
	},
}
