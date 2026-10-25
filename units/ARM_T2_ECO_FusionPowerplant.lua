-- ARM_T2_ECO_FusionPowerplant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_eco_fusionpowerplant = {
		-- id
		name = "Fusion Powerplant",
		description = "Produces Energy",
		side = "ARM",
		unitname = "arm_t2_eco_fusionpowerplant",
		objectname = "ARM_T2_ECO_FusionPowerplant.s3o",
		script = "ARM_T2_ECO_FusionPowerplant.lua",
		corpse = "ARM_T2_ECO_FusionPowerplant_dead",
		icontype = "building_energy_source_big",
		category = "ARM LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 36058,
		buildcostmetal = 5130,
		buildtime = 93768,
		energymake = 1000,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 3100,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 367,
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
				"fusion1",
			},
			underattack = "warning1",
		},
	},
}
