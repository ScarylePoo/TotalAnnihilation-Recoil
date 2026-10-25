-- ARM_Commander (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_commander = {
		-- id
		name = "Commander",
		description = "Commander",
		side = "ARM",
		unitname = "arm_commander",
		buildoptions = Shared.buildListArmCommander,
		objectname = "ARM_Commander",
		icontype = "commander",
		category = "ARM COMMANDER LEVEL10 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 34125,
		buildcostmetal = 29854,
		buildtime = 95897,
		-- resources
		energymake = 25,
		metalmake = 1,
		energystorage = 1050,
		metalstorage = 1050,
		-- movement or placement
		movementclass = "COMMANDER",
		movestate = 1,
		canmove = 1,
		canpatrol = 1,
		canguard = 1,
		maxvelocity = 1.8,
		brakerate = 0.3,
		acceleration = 0.5,
		turnrate = 1044,
		-- nanolathing
		builder = 1,
		workertime = 300,
		builddistance = 128,
		cancapture = 1,
		-- combat
		candgun = 1,
		firestate = 2,
		badtargetcategory = "VTOL",
		nochasecategory = "VTOL",
		explodeas = "COMMANDER_EXPLOSION",
		selfdestructas = "COMMANDER_EXPLOSION",
		-- properties
		showplayername = 1,
		commander = 1,
		maxdamage = 3500,
		hidedamage = 1,
		mass = 2999,  -- so it's transportable damnit
		sightdistance = 500,
		radardistance = 700,
		sonardistance = 700,
		-- other abilities
		activatewhenbuilt = 1,
		cloakcost = 200,
		cloakcostmoving = 1000,
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
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		healtime = 27,
		immunetoparalyzer = 1,
		norestrict = 1,
		ovradjust = 1,
		steeringmode = 2,
		customparams = {
			iscommander = 1,
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
			[1] = {
				name = "COMMANDER_LASER",
			},
			[3] = {
				name = "DISINTEGRATOR",
			},
		},
	},
}
