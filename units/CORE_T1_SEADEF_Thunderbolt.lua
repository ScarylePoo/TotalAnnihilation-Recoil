-- CORE_T1_SEADEF_Thunderbolt (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seadef_thunderbolt = {
		-- id
		name = "Thunderbolt",
		description = "Floating Heavy Laser Tower",
		side = "CORE",
		unitname = "core_t1_seadef_thunderbolt",
		objectname = "CORE_T1_SEADEF_Thunderbolt.s3o",
		buildpic = "CORE_T1_SEADEF_Thunderbolt.png",
		script = "CORE_T1_SEADEF_Thunderbolt.lua",
		corpse = "CORE_T1_SEADEF_Thunderbolt_dead",
		category = "CORE SPECIAL LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5812,
		buildcostmetal = 558,
		buildtime = 12651,
		energyuse = 0.1,  -- TA 3.1c (was unset)
		energystorage = 200,  -- TA 3.1c (was unset)
		-- movement or placement
		minwaterdepth = 5,
		-- combat
		firestate = 2,
		badtargetcategory = "NOTAIR",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1385,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 360,  -- TA 3.1c (was 665)
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		waterline = 15,
		footprintx = 3,
		footprintz = 3,
		yardmap = "www www www",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
		defaultmissiontype = "GUARD_NOMOVE",
		buildangle = 16384,
		noshadow = 1,
		sounds = {
			arrived = {
				"kbcorstp",
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
				"kbcormov",
			},
			select = {
				"kbcorsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "CORE_FLOATING_HEAVY_LASER",
			},
		},
	},
}
