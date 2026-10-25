-- ARM_T2_DEF_TargetingFacility (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_targetingfacility = {
		-- id
		name = "Targeting Facility",
		description = "Automatic Radar Targeting",
		side = "ARM",
		unitname = "arm_t2_def_targetingfacility",
		objectname = "ARM_T2_DEF_TargetingFacility",
		corpse = "ARM_T2_DEF_TargetingFacility_dead",
		icontype = "building",
		category = "ARM SPECIAL LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 90000,
		buildcostmetal = 3600,
		buildtime = 154785,
		energyuse = 1250,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDING",
		-- properties
		maxdamage = 1900,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		damagemodifier = 0.7,
		istargetingupgrade = 1,
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
			activate = "targon1",
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			deactivate = "targoff1",
			select = {
				"targsel1",
			},
			underattack = "warning1",
			working = "targsel1",
		},
	},
}
