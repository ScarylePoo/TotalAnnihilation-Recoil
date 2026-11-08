-- Feature definitions (converted from ARM_T1_SEAPL_Albatross_dead.tdf)

return {
	arm_t1_seapl_albatross_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_SEAPL_Albatross_dead.s3o",
		featuredead = "ARM_T1_SEAPL_Albatross_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 446,  -- TA rule: 0.8 x unit metal 557 (was 186)
		damage = 173,  -- TA rule: 0.8 x unit HP 216 (was 300)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t1_seapl_albatross_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3c.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 223,  -- TA rule: half of its wreck (was 91)
		damage = 173,  -- TA rule: = its wreck (was 150)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
