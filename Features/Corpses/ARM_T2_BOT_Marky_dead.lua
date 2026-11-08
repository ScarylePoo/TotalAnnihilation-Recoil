-- Feature definitions (converted from ARM_T2_BOT_Marky_dead.tdf)

return {
	arm_t2_bot_marky_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_BOT_Marky_dead.s3o",
		featuredead = "ARM_T2_BOT_Marky_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 76,
		damage = 256,  -- TA 3.1c (was 64)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_bot_marky_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2a.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 38,
		damage = 128,  -- TA 3.1c (was 32)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
