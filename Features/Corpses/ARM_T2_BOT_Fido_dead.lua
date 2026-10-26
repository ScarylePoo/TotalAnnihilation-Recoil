-- Feature definitions (converted from ARM_T2_BOT_Fido_dead.tdf)

return {
	arm_t2_bot_fido_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_BOT_Fido_dead.s3o",
		featuredead = "ARM_T2_BOT_Fido_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 318,
		damage = 199,  -- 800
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_bot_fido_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2a",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 159,
		damage = 199,  -- 800
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
