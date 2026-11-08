-- Feature definitions (converted from ARM_T2_SEA_Millenium_dead.tdf)

return {
	arm_t2_sea_millenium_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_SEA_Millenium_dead.s3o",
		footprintx = 6,
		footprintz = 6,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 3523,
		damage = 24000,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T2_SEA_Millenium_heap",
	},
	arm_t2_sea_millenium_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "7x7b.s3o",
		footprintx = 7,
		footprintz = 7,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 1762,
		damage = 24000,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
