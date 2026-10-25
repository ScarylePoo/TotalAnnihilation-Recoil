-- ARM_T2_ECO_MohoMetalMaker (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_eco_mohometalmaker = {
		-- id
		name = "Moho Metal Maker",
		description = "Converts Energy into Metal",
		side = "ARM",
		unitname = "arm_t2_eco_mohometalmaker",
		objectname = "ARM_T2_ECO_MohoMetalMaker",
		corpse = "ARM_T2_ECO_MohoMetalMaker_dead",
		icontype = "building_metal_source_big",
		category = "ARM LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 29350,
		buildcostmetal = 158,
		buildtime = 104980,
		makesmetal = 16,
		energyuse = 800,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 400,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 376,
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
			activate = "metlon1",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "metloff1",
			select = {
				"metlon1",
			},
			underattack = "warning1",
			working = "metlrun1",
		},
	},
}
