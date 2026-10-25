-- Feature definitions (converted from CORE_T2_ECO_FusionPowerplant_dead.tdf)

return {
	core_t2_eco_fusionpowerplant_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_ECO_FusionPowerplant_dead",
		featuredead = "CORE_T2_ECO_FusionPowerplant_heap",
		footprintx = 5,
		footprintz = 5,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 4003,
		damage = 600,  -- 2400
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_eco_fusionpowerplant_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "5x5d",
		footprintx = 5,
		footprintz = 5,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 2002,
		damage = 600,  -- 2400
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
