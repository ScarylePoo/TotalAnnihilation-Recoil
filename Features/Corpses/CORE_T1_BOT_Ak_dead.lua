-- Feature definitions (converted from CORE_T1_BOT_Ak_dead.tdf)

return {
	core_t1_bot_ak_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_BOT_Ak_dead.s3o",
		featuredead = "CORE_T1_BOT_Ak_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 45,
		damage = 212,  -- TA 3.1c (was 52)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_bot_ak_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2c.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 22,
		damage = 212,  -- TA 3.1c (was 55)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
