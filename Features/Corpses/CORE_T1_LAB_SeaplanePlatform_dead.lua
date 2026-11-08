-- Feature definitions (converted from CORE_T1_LAB_SeaplanePlatform_dead.tdf)

return {
	core_t1_lab_seaplaneplatform_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_LAB_SeaplanePlatform_dead.s3o",
		footprintx = 7,
		footprintz = 7,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 1844,  -- TA 3.1c (was 1444)
		damage = 1600,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T1_LAB_SeaplanePlatform_heap",
	},
	core_t1_lab_seaplaneplatform_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "7x7a.s3o",
		footprintx = 7,
		footprintz = 7,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 922,  -- TA rule: half of its wreck (was 722)
		damage = 1600,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
