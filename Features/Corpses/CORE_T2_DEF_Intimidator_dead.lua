-- Feature definitions (converted from CORE_T2_DEF_Intimidator_dead.tdf)

return {
	core_t2_def_intimidator_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_DEF_Intimidator_dead.s3o",
		featuredead = "CORE_T2_DEF_Intimidator_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 4267,
		damage = 1520,  -- TA 3.1c (was 379)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_def_intimidator_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3c.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 2133,
		damage = 1520,  -- TA 3.1c (was 383)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
