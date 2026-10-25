-- CORE_T1_ECO_WindGenerator (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_eco_windgenerator = {
		-- id
		name = "Wind Generator",
		description = "Produces Energy",
		side = "CORE",
		unitname = "core_t1_eco_windgenerator",
		objectname = "CORE_T1_ECO_WindGenerator.s3o",
		corpse = "CORE_T1_ECO_WindGenerator_dead",
		icontype = "building",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 323,
		buildcostmetal = 55,
		buildtime = 1687,
		windgenerator = 30,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 30,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 179,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
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
		ovradjust = 1,
		sounds = {
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
				"windgen2",
			},
			underattack = "warning1",
		},
	},
}
