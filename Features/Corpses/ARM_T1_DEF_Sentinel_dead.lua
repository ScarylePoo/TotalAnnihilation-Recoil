-- Feature definitions (converted from ARM_T1_DEF_Sentinel_dead.tdf)

return {
	arm_t1_def_sentinel_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_DEF_Sentinel_dead.s3o",
		featuredead = "ARM_T1_DEF_Sentinel_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 467,
		damage = 984,  -- TA 3.1c (was 246)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t1_def_sentinel_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2a.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 234,
		damage = 984,  -- TA 3.1c (was 246)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
