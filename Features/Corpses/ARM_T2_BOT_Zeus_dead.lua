-- Feature definitions (converted from ARM_T2_BOT_Zeus_dead.tdf)

return {
	arm_t2_bot_zeus_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_BOT_Zeus_dead",
		featuredead = "ARM_T2_BOT_Zeus_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 214,
		damage = 175,  -- 700
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_bot_zeus_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2e",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 107,
		damage = 175,  -- 700
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
