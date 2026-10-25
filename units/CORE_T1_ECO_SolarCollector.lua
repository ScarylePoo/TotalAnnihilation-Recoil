-- CORE_T1_ECO_SolarCollector (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_eco_solarcollector = {
		-- id
		name = "Solar Collector",
		description = "Produces Energy",
		side = "CORE",
		unitname = "core_t1_eco_solarcollector",
		objectname = "CORE_T1_ECO_SolarCollector",
		corpse = "CORE_T1_ECO_SolarCollector_dead",
		icontype = "building",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 100,
		buildcostmetal = 141,
		buildtime = 2416,
		energyuse = -20,  -- needed to be like this to get the solar stop making energy when deactivated
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "SMALL_BUILDINGEX",
		selfdestructas = "SMALL_BUILDING",
		-- properties
		maxdamage = 320,
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
		buildangle = 32768,
		ovradjust = 1,
		sounds = {
			activate = "solar2",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "solar2",
			select = {
				"solar2",
			},
			underattack = "warning1",
		},
	},
}
