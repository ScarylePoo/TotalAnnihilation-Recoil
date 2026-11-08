-- ARM_T2_SEA_Fibber (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_sea_fibber = {
		-- id
		name = "Fibber",
		description = "Sonar Jamming Sub",
		side = "ARM",
		unitname = "arm_t2_sea_fibber",
		objectname = "ARM_T2_SEA_Fibber.s3o",
		buildpic = "ARM_T2_SEA_Fibber.png",
		script = "ARM_T2_SEA_Fibber.lua",
		corpse = "ARM_T2_SEA_Fibber_dead",
		icontype = "ship",
		category = "ARM UNDERWATER LEVEL2 NOWEAPON NOTAIR",
		-- costs, makes, uses, storage
		buildcostenergy = 2897,
		buildcostmetal = 295,
		buildtime = 11048,
		energyuse = 0.5,  -- TA 3.1c (was 25)
		energymake = 0.5,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "SHIP_SUBMARINE",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.4,
		brakerate = 0.36,
		acceleration = 0.2,
		turnrate = 622,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 450,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 150,  -- TA 3.1c (was 260)
		sonardistancejam = 650,  -- TA 3.1c (was 850)
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		waterline = 40,
		footprintx = 3,
		footprintz = 3,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		sounds = {
			arrived = {
				"suarmstp",
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
				"suarmmov",
			},
			select = {
				"watrjam1",
			},
			underattack = "warning1",
		},
	},
}
