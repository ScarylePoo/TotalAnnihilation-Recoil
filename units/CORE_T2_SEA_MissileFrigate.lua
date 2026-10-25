-- CORE_T2_SEA_MissileFrigate (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_sea_missilefrigate = {
		-- id
		name = "Missile Frigate",
		description = "Missile Ship",
		side = "CORE",
		unitname = "core_t2_sea_missilefrigate",
		objectname = "CORE_T2_SEA_MissileFrigate",
		corpse = "CORE_T2_SEA_MissileFrigate_dead",
		icontype = "ship",
		category = "CORE SHIP LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 7628,
		buildcostmetal = 2283,
		buildtime = 22126,
		-- movement or placement
		movementclass = "MEDIUM_SHIP",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		floater = 1,
		maxvelocity = 1.4,
		brakerate = 0.038,
		acceleration = 0.02,
		turnrate = 256,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1250,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 428,
		radardistance = 2000,
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		footprintx = 6,
		footprintz = 6,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		steeringmode = 1,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		ovradjust = 1,
		sounds = {
			arrived = {
				"shcorstp",
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
				"shcormov",
			},
			select = {
				"shcorsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORE_SHIP_ROCKET",
				onlytargetcategory = "NOTAIR",
			},
			{
				name = "CORSHIP_MISSILE",
			},
		},
	},
}
