-- Feature definitions (converted from ARM_T2_SEA_Conqueror_dead.tdf)

return {
	arm_t2_sea_conqueror_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_SEA_Conqueror_dead.s3o",
		footprintx = 5,
		footprintz = 5,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 1375,
		damage = 24000,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T2_SEA_Conqueror_heap",
	},
	arm_t2_sea_conqueror_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "6x6b.s3o",
		footprintx = 6,
		footprintz = 6,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 688,
		damage = 24000,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
