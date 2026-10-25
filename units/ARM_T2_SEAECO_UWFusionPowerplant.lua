-- ARM_T2_SEAECO_UWFusionPowerplant (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_seaeco_uwfusionpowerplant = {
		-- id
		name = "Underwater Fusion Powerplant",
		description = "Produces Energy",
		side = "ARM",
		unitname = "arm_t2_seaeco_uwfusionpowerplant",
		objectname = "ARM_T2_SEAECO_UWFusionPowerplant",
		script = "ARM_T2_SEAECO_UWFusionPowerplant.lua",
		corpse = "ARM_T2_SEAECO_UWFusionPowerplant_dead",
		icontype = "building_energy_source_big",
		category = "ARM LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 54287,
		buildcostmetal = 7085,
		buildtime = 131255,
		energymake = 1150,
		-- movement or placement
		minwaterdepth = 15,
		maxwaterdepth = 255,
		maxslope = 10,
		-- combat
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "NUCLEAR_MISSILE",
		-- properties
		maxdamage = 1231,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 190,
		-- unit animation
		footprintx = 5,
		footprintz = 4,
		yardmap = "ooooo ooooo ooooo ooooo",
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
				"watfusn1",
			},
			underattack = "warning1",
		},
	},
}
