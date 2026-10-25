-- ARM_T1_VEH_Flash (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_veh_flash = {
		-- id
		name = "Flash",
		description = "Fast Assault Tank",
		side = "ARM",
		unitname = "arm_t1_veh_flash",
		objectname = "ARM_T1_VEH_Flash.s3o",
		corpse = "ARM_T1_VEH_Flash_dead",
		icontype = "tank",
		category = "ARM TANK LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 870,
		buildcostmetal = 106,
		buildtime = 1676,
		-- movement or placement
		movementclass = "TANKSH2",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 2.7,
		brakerate = 0.04,
		acceleration = 0.135,
		turnrate = 575,
		maxwaterdepth = 12,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 500,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 393,
		-- unit animation
		leavetracks = 1,
		trackwidth = 24,
		trackoffset = 3,
		trackstrength = 5,
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
				name = "EMG",
			},
		},
	},
}
