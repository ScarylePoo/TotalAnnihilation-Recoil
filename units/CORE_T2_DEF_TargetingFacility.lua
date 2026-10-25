-- CORE_T2_DEF_TargetingFacility (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_targetingfacility = {
		-- id
		name = "Targeting Facility",
		description = "Automatic Radar Targeting",
		side = "CORE",
		unitname = "core_t2_def_targetingfacility",
		objectname = "CORE_T2_DEF_TargetingFacility",
		corpse = "CORE_T2_DEF_TargetingFacility_dead",
		icontype = "building",
		category = "CORE SPECIAL LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 90000,
		buildcostmetal = 3680,
		buildtime = 161287,
		energyuse = 1300,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 1800,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		istargetingupgrade = 1,
		damagemodifier = 0.7,
		-- unit animation
		footprintx = 5,
		footprintz = 4,
		yardmap = "ooooo ooooo ooooo ooooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 4096,
		sounds = {
			activate = "targon2",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "targoff2",
			select = {
				"targsel2",
			},
			underattack = "warning1",
			working = "targsel2",
		},
	},
}
