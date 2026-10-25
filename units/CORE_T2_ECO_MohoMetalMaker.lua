-- CORE_T2_ECO_MohoMetalMaker (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_eco_mohometalmaker = {
		-- id
		name = "Moho Metal Maker",
		description = "Converts Energy into Metal",
		side = "CORE",
		unitname = "core_t2_eco_mohometalmaker",
		objectname = "CORE_T2_ECO_MohoMetalMaker",
		corpse = "CORE_T2_ECO_MohoMetalMaker_dead",
		icontype = "building_metal_source_big",
		category = "CORE LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 10928,
		buildcostmetal = 151,
		buildtime = 121253,
		makesmetal = 12,
		energyuse = 625,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 500,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		damagemodifier = 0.7,
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
		sounds = {
			activate = "metlon2",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "metloff2",
			select = {
				"metlon2",
			},
			underattack = "warning1",
			working = "metlrun2",
		},
	},
}
