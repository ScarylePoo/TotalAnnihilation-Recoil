-- CORE_T2_ECO_CloakableFusion (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_eco_cloakablefusion = {
		-- id
		name = "Cloakable Fusion Powerplant",
		description = "Produces Energy",
		side = "CORE",
		unitname = "core_t2_eco_cloakablefusion",
		objectname = "CORE_T2_ECO_CloakableFusion",
		corpse = "CORE_T2_ECO_CloakableFusion_dead",
		icontype = "building_energy_source_big",
		category = "CORE LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 46225,
		buildcostmetal = 5321,
		buildtime = 111874,
		energymake = 1050,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 2450,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 376,
		-- other abilities
		cloakcost = 550,
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
				"fusion2",
			},
			underattack = "warning1",
		},
	},
}
