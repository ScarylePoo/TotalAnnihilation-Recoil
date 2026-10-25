-- Feature definitions (converted from ARM_T1_SEAECO_UWEnergyStorage_dead.tdf)

return {
	arm_t1_seaeco_uwenergystorage_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_SEAECO_UWEnergyStorage_dead",
		featuredead = "ARM_T1_SEAECO_UWEnergyStorage_heap",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 227,
		damage = 293,  -- 1158
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t1_seaeco_uwenergystorage_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4b",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 113,
		damage = 153,  -- 579
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
