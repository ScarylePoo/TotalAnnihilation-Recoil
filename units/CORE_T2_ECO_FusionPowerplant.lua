-- CORE_T2_ECO_FusionPowerplant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_eco_fusionpowerplant = {
		-- id
		name = "Fusion Powerplant",
		description = "Produces Energy",
		side = "CORE",
		unitname = "core_t2_eco_fusionpowerplant",
		objectname = "CORE_T2_ECO_FusionPowerplant",
		corpse = "CORE_T2_ECO_FusionPowerplant_dead",
		icontype = "building_energy_source_big",
		category = "CORE LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 37865,
		buildcostmetal = 5004,
		buildtime = 94281,
		energymake = 1050,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 3000,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
		-- unit animation
		footprintx = 5,
		footprintz = 5,
		yardmap = "ooooo ooooo ooooo ooooo ooooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 16384,
		ovradjust = 1,
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
