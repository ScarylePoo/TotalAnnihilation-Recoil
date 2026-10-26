-- ARM_T2_VEH_Jammer (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_jammer = {
		-- id
		name = "Jammer",
		description = "Mobile Radar Jammer",
		side = "ARM",
		unitname = "arm_t2_veh_jammer",
		objectname = "ARM_T2_VEH_Jammer.s3o",
		corpse = "ARM_T2_VEH_Jammer_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1621,
		buildcostmetal = 97,
		buildtime = 5933,
		energyuse = 16,
		-- movement or placement
		movementclass = "TANKSH2",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.2,
		brakerate = 0.012,
		acceleration = 0.035,
		turnrate = 505,
		maxwaterdepth = 0,
		maxslope = 16,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 460,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 420,
		radardistancejam = 500,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		leavetracks = 1,
		trackwidth = 22,
		trackoffset = 8,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "VehTrack",
		footprintx = 2,
		footprintz = 2,
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
			activate = "radjam1",
			arrived = {
				"varmstop",
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
			deactivate = "radjam1",
			ok = {
				"varmmove",
			},
			select = {
				"radjam1",
			},
			underattack = "warning1",
		},
	},
}
