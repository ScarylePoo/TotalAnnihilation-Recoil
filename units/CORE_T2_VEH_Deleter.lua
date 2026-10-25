-- CORE_T2_VEH_Deleter (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_veh_deleter = {
		-- id
		name = "Deleter",
		description = "Mobile Radar Jammer",
		side = "CORE",
		unitname = "core_t2_veh_deleter",
		objectname = "CORE_T2_VEH_Deleter",
		corpse = "CORE_T2_VEH_Deleter_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1757,
		buildcostmetal = 100,
		buildtime = 6404,
		energyuse = 14,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.25,
		brakerate = 0.014,
		acceleration = 0.031,
		turnrate = 512,
		maxwaterdepth = 0,
		maxslope = 16,
		-- combat
		badtargetcategory = "VTOL NOTAIR",
		nochasecategory = "VTOL NOTAIR",
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 520,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 390,
		radardistancejam = 520,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		leavetracks = 1,
		trackwidth = 27,
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
		ovradjust = 1,
		sounds = {
			activate = "radjam2",
			arrived = {
				"vcorstop",
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
			deactivate = "radjam2",
			ok = {
				"vcormove",
			},
			select = {
				"radjam2",
			},
			underattack = "warning1",
		},
	},
}
