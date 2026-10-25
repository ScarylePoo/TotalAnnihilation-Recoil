-- CORE_T1_VEH_Spoiler (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_veh_spoiler = {
		-- id
		name = "Spoiler",
		description = "Mine Layer Vehicle",
		side = "CORE",
		unitname = "core_t1_veh_spoiler",
		buildoptions = Shared.buildListCoreMineLayer,
		objectname = "CORE_T1_VEH_Spoiler",
		corpse = "CORE_T1_VEH_Spoiler_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1117,
		buildcostmetal = 187,
		buildtime = 1740,
		-- movement or placement
		movementclass = "TANKSH3",
		movestate = -1,
		canmove = 1,
		canpatrol = 0,
		canguard = 0,
		maxvelocity = 1.1,
		brakerate = 0.2,
		acceleration = 0.01,
		turnrate = 230,
		maxwaterdepth = 0,
		maxslope = 16,
		-- nanolathing
		builder = 1,
		workertime = 120,
		builddistance = 70,
		canassist = 0,
		canreclaim = 0,
		canrepair = 0,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1400,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 254,
		-- unit animation
		leavetracks = 1,
		trackwidth = 24,
		trackoffset = 3,
		trackstrength = 5,
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
				"vcorstop",
			},
			build = "nanlath2",
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
				"vcormove",
			},
			repair = "repair2",
			select = {
				"vcorsel",
			},
			underattack = "warning1",
			working = "reclaim1",
		},
	},
}
