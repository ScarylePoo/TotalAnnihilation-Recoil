-- CORE_T2_SEAECO_UWFusionPowerplant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_seaeco_uwfusionpowerplant = {
		-- id
		name = "Underwater Fusion Powerplant",
		description = "Produces Energy",
		side = "CORE",
		unitname = "core_t2_seaeco_uwfusionpowerplant",
		objectname = "CORE_T2_SEAECO_UWFusionPowerplant",
		corpse = "CORE_T2_SEAECO_UWFusionPowerplant_dead",
		icontype = "building_energy_source_big",
		category = "CORE LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 57349,
		buildcostmetal = 7210,
		buildtime = 124838,
		energymake = 1200,
		-- movement or placement
		minwaterdepth = 15,
		maxwaterdepth = 255,
		maxslope = 10,
		-- combat
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 1425,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 190,
		-- unit animation
		footprintx = 5,
		footprintz = 5,
		yardmap = "ooooo ooooo ooooo ooooo ooooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
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
				"watfusn2",
			},
			underattack = "warning1",
		},
	},
}
