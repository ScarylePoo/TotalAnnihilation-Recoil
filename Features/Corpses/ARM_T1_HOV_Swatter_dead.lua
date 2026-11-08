-- Feature definitions (converted from ARM_T1_HOV_Swatter_dead.tdf)

return {
	arm_t1_hov_swatter_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_HOV_Swatter_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 96,
		damage = 300,  -- TA 3.1c (was 75)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_HOV_Swatter_heap",
	},
	arm_t1_hov_swatter_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3e.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 48,
		damage = 300,  -- TA rule: = its wreck (was 75)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
