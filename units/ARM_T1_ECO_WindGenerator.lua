-- ARM_T1_ECO_WindGenerator (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_eco_windgenerator = {
		-- id
		name = "Wind Generator",
		description = "Produces Energy",
		side = "ARM",
		unitname = "arm_t1_eco_windgenerator",
		objectname = "ARM_T1_ECO_WindGenerator.s3o",
		script = "ARM_T1_ECO_WindGenerator.lua",
		corpse = "ARM_T1_ECO_WindGenerator_dead",
		icontype = "building",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 312,
		buildcostmetal = 52,
		buildtime = 1603,
		windgenerator = 30,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 30,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 176,
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
		buildangle = 8192,
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
				"windgen1",
			},
			underattack = "warning1",
		},
	},
}
