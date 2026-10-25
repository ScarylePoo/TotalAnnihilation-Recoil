-- CORE_T2_VEH_Reaper (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_veh_reaper = {
		-- id
		name = "Reaper",
		description = "Heavy Assault Tank",
		side = "CORE",
		unitname = "core_t2_veh_reaper",
		objectname = "CORE_T2_VEH_Reaper.s3o",
		corpse = "CORE_T2_VEH_Reaper_dead",
		icontype = "tank",
		category = "CORE TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3048,
		buildcostmetal = 573,
		buildtime = 6730,
		-- movement or placement
		movementclass = "HEAVYTANK",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.45,
		brakerate = 0.008,
		acceleration = 0.011,
		turnrate = 299,
		maxwaterdepth = 10,
		maxslope = 12,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "HUGE_UNITEX",
		selfdestructas = "HUGE_UNITEX",
		-- properties
		maxdamage = 2500,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 420,
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
		ovradjust = 1,
		sounds = {
			arrived = {
				"tcorst0p",
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
				"tcormove",
			},
			select = {
				"tcorsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORE_REAP",
			},
		},
	},
}
