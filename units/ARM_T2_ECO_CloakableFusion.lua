-- ARM_T2_ECO_CloakableFusion (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_eco_cloakablefusion = {
		-- id
		name = "Cloakable Fusion Powerplant",
		description = "Produces Energy",
		side = "ARM",
		unitname = "arm_t2_eco_cloakablefusion",
		objectname = "ARM_T2_ECO_CloakableFusion",
		script = "ARM_T2_ECO_CloakableFusion.lua",
		corpse = "ARM_T2_ECO_CloakableFusion_dead",
		icontype = "building_energy_source_big",
		category = "ARM LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 39058,
		buildcostmetal = 5420,
		buildtime = 105487,
		energymake = 1000,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 3200,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 368,
		-- other abilities
		cloakcost = 450,
		mincloakdistance = 110,
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
		initcloaked = 1,
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
				"fusion1",
			},
			underattack = "warning1",
		},
	},
}
