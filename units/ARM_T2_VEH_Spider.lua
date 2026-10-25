-- ARM_T2_VEH_Spider (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_spider = {
		-- id
		name = "Spider",
		description = "Spider Assault Vehicle",
		side = "ARM",
		unitname = "arm_t2_veh_spider",
		objectname = "ARM_T2_VEH_Spider",
		corpse = "ARM_T2_VEH_Spider_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2000,
		buildcostmetal = 230,
		buildtime = 5075,
		-- movement or placement
		movementclass = "SPID3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.7,
		brakerate = 0.15,
		acceleration = 0.17,
		turnrate = 1020,
		maxwaterdepth = 12,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 450,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 468,
		-- unit animation
		leavetracks = 1,
		trackwidth = 45,
		trackoffset = 0,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "SpidTrack",
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
		ovradjust = 1,
		sounds = {
			arrived = {
				"spider",
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
				"spider",
			},
			select = {
				"spider",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_PARALYZER",
			},
		},
	},
}
