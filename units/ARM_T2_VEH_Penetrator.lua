-- ARM_T2_VEH_Penetrator (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_penetrator = {
		-- id
		name = "Penetrator",
		description = "Mobile Energy Weapon",
		side = "ARM",
		unitname = "arm_t2_veh_penetrator",
		objectname = "ARM_T2_VEH_Penetrator",
		corpse = "ARM_T2_VEH_Penetrator_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 14477,
		buildcostmetal = 2004,
		buildtime = 35706,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = .6,
		brakerate = 0.07,
		acceleration = 0.01,
		turnrate = 230,
		maxwaterdepth = 0,
		maxslope = 12,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "CRAWL_BLASTEX",
		selfdestructas = "ATOMIC_BLAST",
		-- properties
		maxdamage = 650,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 455,
		-- unit animation
		leavetracks = 1,
		trackwidth = 40,
		trackoffset = 8,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "VehTrack",
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
				"tarmst0p",
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
				"tarmmove",
			},
			select = {
				"tarmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "PENETRATOR_ANNIHILATOR_BEAM",
			},
		},
	},
}
