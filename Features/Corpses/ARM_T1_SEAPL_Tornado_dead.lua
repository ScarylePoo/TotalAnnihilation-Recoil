-- Feature definitions (converted from ARM_T1_SEAPL_Tornado_dead.tdf)

return {
	arm_t1_seapl_tornado_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_SEAPL_Tornado_dead.s3o",
		featuredead = "ARM_T1_SEAPL_Tornado_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 150,  -- TA rule: 0.8 x unit metal 187 (was 157)
		damage = 120,  -- TA rule: 0.8 x unit HP 150 (was 300)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t1_seapl_tornado_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3c.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 75,  -- TA rule: half of its wreck (was 68)
		damage = 120,  -- TA rule: = its wreck (was 150)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
