-- ARM_T2_VEH_Triton (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_triton = {
		-- id
		name = "Triton",
		description = "Amphibious Tank",
		side = "ARM",
		unitname = "arm_t2_veh_triton",
		objectname = "ARM_T2_VEH_Triton.s3o",
		corpse = "ARM_T2_VEH_Triton_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2900,
		buildcostmetal = 345,
		buildtime = 6112,
		-- movement or placement
		movementclass = "AMPHTANK",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.3,
		brakerate = 0.008,
		acceleration = 0.017,
		turnrate = 370,
		maxwaterdepth = 255,
		maxslope = 12,
		-- combat
		firestate = -1,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 2230,
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
				name = "ARM_MEDIUMCANNON",
			},
		},
	},
}
