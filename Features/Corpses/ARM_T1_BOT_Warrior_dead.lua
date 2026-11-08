-- Feature definitions (converted from ARM_T1_BOT_Warrior_dead.tdf)

return {
	arm_t1_bot_warrior_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_BOT_Warrior_dead.s3o",
		featuredead = "ARM_T1_BOT_Warrior_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 157,
		damage = 680,  -- TA 3.1c (was 163)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t1_bot_warrior_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2a.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 79,
		damage = 340,  -- TA 3.1c (was 87)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
