-- Feature definitions (converted from ARM_T2_BOT_Shooter_dead.tdf)

return {
	arm_t2_bot_shooter_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_BOT_Shooter_dead.s3o",
		featuredead = "ARM_T2_BOT_Shooter_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 748,
		damage = 400,  -- TA 3.1c (was 97)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_bot_shooter_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2d.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 374,
		damage = 200,  -- TA 3.1c (was 45)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
