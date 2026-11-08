-- Feature definitions (converted from CORE_T1_SEAECO_UWMetalStorage_dead.tdf)

return {
	core_t1_seaeco_uwmetalstorage_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_SEAECO_UWMetalStorage_dead.s3o",
		featuredead = "CORE_T1_SEAECO_UWMetalStorage_heap",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 280,
		damage = 1400,  -- TA 3.1c (was 344)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_seaeco_uwmetalstorage_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4d.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 140,
		damage = 700,  -- TA 3.1c (was 166)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
