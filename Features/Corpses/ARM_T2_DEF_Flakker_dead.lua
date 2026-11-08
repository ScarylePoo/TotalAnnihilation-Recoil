-- Feature definitions (converted from ARM_T2_DEF_Flakker_dead.tdf)

return {
	arm_t2_def_flakker_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_DEF_Flakker_dead.s3o",
		featuredead = "ARM_T2_DEF_Flakker_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 855,
		damage = 1219,  -- TA 3.1c (was 303)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_def_flakker_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2c.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 428,
		damage = 609,  -- TA 3.1c (was 152)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
