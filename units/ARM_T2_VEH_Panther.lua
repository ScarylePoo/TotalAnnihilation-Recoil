-- ARM_T2_VEH_Panther (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_veh_panther = {
		-- id
		name = "Panther",
		description = "Lightning Tank",
		side = "ARM",
		unitname = "arm_t2_veh_panther",
		objectname = "ARM_T2_VEH_Panther",
		corpse = "ARM_T2_VEH_Panther_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3830,
		buildcostmetal = 284,
		buildtime = 9676,
		-- movement or placement
		movementclass = "TANKSH2",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.8,
		brakerate = 0.025,
		acceleration = 0.07,
		turnrate = 475,
		maxwaterdepth = 12,
		maxslope = 10,
		-- combat
		firestate = 2,
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1100,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 446,
		-- unit animation
		leavetracks = 1,
		trackwidth = 27,
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
				badtargetcategory = "VTOL",
				name = "armlatnk_weapon",
			},
			{
				name = "armkbot_missile",
			},
		},
	},
}
