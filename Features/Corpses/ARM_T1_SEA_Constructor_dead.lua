-- Feature definitions (converted from ARM_T1_SEA_Constructor_dead.tdf)

return {
	arm_t1_sea_constructor_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_SEA_Constructor_dead.s3o",
		footprintx = 5,
		footprintz = 5,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 244,
		damage = 24000,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_SEA_Constructor_heap",
	},
	arm_t1_sea_constructor_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4f.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 122,
		damage = 24000,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
