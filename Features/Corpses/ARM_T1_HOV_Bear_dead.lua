-- Feature definitions (converted from ARM_T1_HOV_Bear_dead.tdf)

return {
	arm_t1_hov_bear_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_HOV_Bear_dead.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 532,
		damage = 920,  -- TA 3.1c (was 223)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_HOV_Bear_heap",
	},
	arm_t1_hov_bear_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4b.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 266,
		damage = 920,  -- TA rule: = its wreck (was 223)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
