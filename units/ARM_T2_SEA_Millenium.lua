-- ARM_T2_SEA_Millenium (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_sea_millenium = {
		-- id
		name = "Millenium",
		description = "Battleship",
		side = "ARM",
		unitname = "arm_t2_sea_millenium",
		objectname = "ARM_T2_SEA_Millenium.s3o",
		buildpic = "ARM_T2_SEA_Millenium.png",
		script = "ARM_T2_SEA_Millenium.lua",
		corpse = "ARM_T2_SEA_Millenium_dead",
		category = "ARM SHIP LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 20731,  -- TA 3.1c (was 25914)
		buildcostmetal = 4404,  -- TA 3.1c (was 5505)
		buildtime = 42730,
		energymake = 50,  -- TA 3.1c (was unset)
		energyuse = 48,  -- TA 3.1c (was unset)
		-- movement or placement
		movementclass = "BIG_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 2,
		brakerate = 0.018,
		acceleration = 0.005,  -- TA 3.1c (was 0.018)
		turnrate = 64,  -- TA 3.1c (was 128)
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 5720,  -- TA 3.1c (was 7720)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 350,  -- TA 3.1c (was 612)
		-- unit animation
		footprintx = 8,
		footprintz = 8,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		scale = 0.6,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		buildangle = 16384,
		ovradjust = 1,
		sounds = {
			arrived = {
				"sharmstp",
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
				"sharmmov",
			},
			select = {
				"sharmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_BATS",
			},
			{
				name = "ARM_BATS",
			},
		},
	},
}
