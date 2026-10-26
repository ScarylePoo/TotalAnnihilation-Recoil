-- ARM_T2_BOT_DecoyCommander (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_bot_decoycommander = {
		-- id
		name = "Decoy",
		description = "Commander",
		side = "ARM",
		unitname = "arm_t2_bot_decoycommander",
		objectname = "ARM_T2_BOT_DecoyCommander.s3o",
		script = "ARM_T2_BOT_DecoyCommander.lua",
		icontype = "kbot",
		category = "ARM KBOT LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 11561,
		buildcostmetal = 721,
		buildtime = 24048,
		-- movement or placement
		movementclass = "COMMANDER",
		movestate = -1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.2,
		brakerate = 0.3,
		acceleration = 0.15,
		turnrate = 1044,
		-- nanolathing
		builder = 1,
		workertime = 30,
		builddistance = 60,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "DECOY_COMMANDER_BLAST",
		selfdestructas = "DECOY_COMMANDER_BLAST",
		-- properties
		showplayername = 1,
		maxdamage = 1420,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 500,
		radardistance = 700,
		sonardistance = 700,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		cloakcost = 50,
		cloakcostmoving = 250,
		mincloakdistance = 40,
		-- unit animation
		upright = 1,
		smoothanim = 1,
		leavetracks = 1,
		trackwidth = 22,
		trackoffset = 0,
		trackstrength = 10,
		trackstretch = 1,
		tracktype = "KbotTrack",
		footprintx = 2,
		footprintz = 2,
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 1,
		threed = 1,
		zbuffer = 1,
		steeringmode = 2,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		customparams = {
			iscommander = 1,
			isdecoycommander = 1,
			side = "arm",
		},
		sounds = {
			arrived = {
				"kcarmstp",
			},
			build = "nanlath1",
			canceldestruct = "cancel2",
			capture = "capture1",
			cloak = "kloak1",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			ok = {
				"kcarmmov",
			},
			repair = "repair1",
			select = {
				"kcarmsel",
			},
			uncloak = "kloak1un",
			underattack = "warning2",
			unitcomplete = "kcarmmov",
			working = "reclaim1",
		},
		weapons = {
			{
				name = "COMMANDER_LASER",
			},
		},
	},
}
