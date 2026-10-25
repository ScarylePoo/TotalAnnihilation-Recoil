-- ARM_T1_ECO_SolarCollector (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_eco_solarcollector = {
		-- id
		name = "Solar Collector",
		description = "Produces Energy",
		side = "ARM",
		unitname = "arm_t1_eco_solarcollector",
		objectname = "ARM_T1_ECO_SolarCollector.s3o",
		script = "ARM_T1_ECO_SolarCollector.lua",
		corpse = "ARM_T1_ECO_SolarCollector_dead",
		icontype = "building",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 75,
		buildcostmetal = 145,
		buildtime = 2495,
		energyuse = -20,  -- needed to be like this to get the solar stop making energy when deactivated
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 326,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		damagemodifier = 0.33,
		-- unit animation
		footprintx = 5,
		footprintz = 5,
		yardmap = "ooooo ooooo ooooo ooooo ooooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 4096,
		ovradjust = 1,
		sounds = {
			activate = "solar1",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "solar1",
			select = {
				"solar1",
			},
			underattack = "warning1",
		},
	},
}
