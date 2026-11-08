-- Feature definitions (converted from CORE_T1_SEAECO_UWMetalExtractor_dead.tdf)

return {
	core_t1_seaeco_uwmetalextractor_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_SEAECO_UWMetalExtractor_dead.s3o",
		featuredead = "CORE_T1_SEAECO_UWMetalExtractor_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 100,
		damage = 284,  -- TA 3.1c (was 167)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_seaeco_uwmetalextractor_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3b.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 50,
		damage = 142,  -- TA 3.1c (was 73)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
