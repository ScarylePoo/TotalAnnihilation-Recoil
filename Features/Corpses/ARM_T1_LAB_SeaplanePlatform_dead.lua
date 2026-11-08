-- Feature definitions (converted from ARM_T1_LAB_SeaplanePlatform_dead.tdf)

return {
	arm_t1_lab_seaplaneplatform_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_LAB_SeaplanePlatform_dead.s3o",
		footprintx = 7,
		footprintz = 7,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 1778,  -- TA 3.1c (was 1478)
		damage = 1456,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_LAB_SeaplanePlatform_heap",
	},
	arm_t1_lab_seaplaneplatform_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "7x7a.s3o",
		footprintx = 7,
		footprintz = 7,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 889,  -- TA rule: half of its wreck (was 739)
		damage = 1456,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
