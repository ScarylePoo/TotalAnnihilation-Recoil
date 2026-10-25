-- Feature definitions (converted from CORE_T1_ECO_EnergyStorage_dead.tdf)

return {
	core_t1_eco_energystorage_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_ECO_EnergyStorage_dead",
		featuredead = "CORE_T1_ECO_EnergyStorage_heap",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 200,
		damage = 214,  -- 856
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_eco_energystorage_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4a",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 100,
		damage = 213,  -- 856
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
