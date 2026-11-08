-- Feature definitions (converted from CORE_T1_SEAECO_UWEnergyStorage_dead.tdf)

return {
	core_t1_seaeco_uwenergystorage_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_SEAECO_UWEnergyStorage_dead.s3o",
		featuredead = "CORE_T1_SEAECO_UWEnergyStorage_heap",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 224,
		damage = 1217,  -- TA 3.1c (was 303)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_seaeco_uwenergystorage_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4d.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 112,
		damage = 609,  -- TA 3.1c (was 151)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
