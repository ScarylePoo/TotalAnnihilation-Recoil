-- Feature definitions (converted from ARM_T1_SEAECO_FloatingMetalMaker_dead.tdf)

return {
	arm_t1_seaeco_floatingmetalmaker_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_SEAECO_FloatingMetalMaker_dead.s3o",
		featurereclamate = "smudge01",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 0,
		damage = 28,  -- 115
		reclaimable = 1,
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_SEAECO_FloatingMetalMaker_heap",
	},
	arm_t1_seaeco_floatingmetalmaker_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3c.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 0,
		damage = 28,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
