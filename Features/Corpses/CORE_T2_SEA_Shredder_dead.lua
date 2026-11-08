-- Feature definitions (converted from CORE_T2_SEA_Shredder_dead.tdf)

return {
	core_t2_sea_shredder_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_SEA_Shredder_dead.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 1051,
		damage = 1960,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T2_SEA_Shredder_heap",
	},
	core_t2_sea_shredder_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4f.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 526,
		damage = 1960,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
