-- CORE_T1_ECO_GeothermalPowerplant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_eco_geothermalpowerplant = {
		-- id
		name = "Geothermal Powerplant",
		description = "Produces Energy",
		side = "CORE",
		unitname = "core_t1_eco_geothermalpowerplant",
		objectname = "CORE_T1_ECO_GeothermalPowerplant.s3o",
		buildpic = "CORE_T1_ECO_GeothermalPowerplant.png",
		script = "CORE_T1_ECO_GeothermalPowerplant.lua",
		corpse = "CORE_T1_ECO_GeothermalPowerplant_dead",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 9375,
		buildcostmetal = 505,
		buildtime = 12875,
		energymake = 250,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 930,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 210,  -- TA 3.1c (was 367)
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "GGGG GGGG GGGG GGGG",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 4096,
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
				"geothrm2",
			},
			underattack = "warning1",
		},
	},
}
