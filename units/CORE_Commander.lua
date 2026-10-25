-- CORE_Commander (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_commander = {
		-- id
		name = "Commander",
		description = "Commander",
		side = "CORE",
		unitname = "core_commander",
		buildoptions = Shared.buildListCoreCommander,
		objectname = "CORE_Commander.s3o",
		icontype = "commander",
		decoyfor = "ARM_Commander",
		category = "CORE COMMANDER LEVEL10 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 35838,
		buildcostmetal = 23512,
		buildtime = 97852,
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
		maxvelocity = 1.6,
		brakerate = 0.32,
		acceleration = 0.5,
		turnrate = 1030,
		-- nanolathing
		builder = 1,
		workertime = 300,
		builddistance = 60,
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
		mass = 2999,  -- for transportableability >:-(
		sightdistance = 515,
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
		steeringmode = 2,
		shootme = 1,
		defaultmissiontype = "Standby",
		maneuverleashlength = 640,
		healtime = 27,
		immunetoparalyzer = 1,
		norestrict = 1,
		ovradjust = 1,
		customparams = {
			iscommander = 1,
			side = "core",
		},
		sounds = {
			arrived = {
				"kccorstp",
			},
			build = "nanlath2",
			canceldestruct = "cancel2",
			capture = "capture2",
			cloak = "kloak2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			ok = {
				"kcormov",
			},
			repair = "repair2",
			select = {
				"kccorsel",
			},
			uncloak = "kloak2un",
			underattack = "warning2",
			unitcomplete = "kccorsel",
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
