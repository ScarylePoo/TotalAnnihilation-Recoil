-- CORE_T2_DEF_AirRepairPad (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_airrepairpad = {
		-- id
		name = "Air Repair Pad",
		description = "Automatically repairs aircraft",
		side = "CORE",
		unitname = "core_t2_def_airrepairpad",
		objectname = "CORE_T2_DEF_AirRepairPad.s3o",
		buildpic = "CORE_T2_DEF_AirRepairPad.png",
		script = "CORE_T2_DEF_AirRepairPad.lua",
		corpse = "CORE_T2_DEF_AirRepairPad_dead",
		icontype = "building",
		category = "CORE LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 8540,
		buildcostmetal = 430,
		buildtime = 21587,
		energymake = 11,  -- TA 3.1c (was unset)
		energystorage = 100,  -- TA 3.1c (was unset)
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- nanolathing
		builder = 1,
		workertime = 200,  -- TA 3.1c (was 800)
		builddistance = 6,
		-- combat
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 690,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 175,  -- TA 3.1c (was 300)
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		isairbase = 1,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 1024,
		sortbias = 0,
		ovradjust = 1,
		sounds = {
			build = "pairwork",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			select = {
				"pairactv",
			},
			underattack = "warning1",
			unitcomplete = "untdone",
		},
	},
}
