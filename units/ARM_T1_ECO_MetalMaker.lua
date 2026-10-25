-- ARM_T1_ECO_MetalMaker (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_eco_metalmaker = {
		-- id
		name = "Metal Maker",
		description = "Converts Energy into Metal",
		side = "ARM",
		unitname = "arm_t1_eco_metalmaker",
		objectname = "ARM_T1_ECO_MetalMaker",
		script = "ARM_T1_ECO_MetalMaker.lua",
		corpse = "ARM_T1_ECO_MetalMaker_dead",
		icontype = "building",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1497,
		buildtime = 2605,
		makesmetal = 1,
		energyuse = 60,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "CRAWL_BLASTEX",
		selfdestructas = "CRAWL_BLASTEX",
		-- properties
		maxdamage = 144,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 360,
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		footprintx = 3,
		footprintz = 3,
		yardmap = "ooooooooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
		ovradjust = 1,
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
