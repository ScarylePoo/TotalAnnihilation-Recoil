-- ARM_T1_ECO_GeothermalPowerplant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_eco_geothermalpowerplant = {
		-- id
		name = "Geothermal Powerplant",
		description = "Produces Energy",
		side = "ARM",
		unitname = "arm_t1_eco_geothermalpowerplant",
		objectname = "ARM_T1_ECO_GeothermalPowerplant",
		script = "ARM_T1_ECO_GeothermalPowerplant.lua",
		corpse = "ARM_T1_ECO_GeothermalPowerplant_dead",
		icontype = "building",
		category = "ARM LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 9568,
		buildcostmetal = 520,
		buildtime = 13078,
		energymake = 250,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "GEO_SPLODE",
		selfdestructas = "GEO_SPLODE",
		-- properties
		maxdamage = 880,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "GGGG GGGG GGGG GGGG",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 2048,
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
				"geothrm1",
			},
			underattack = "warning1",
		},
	},
}
