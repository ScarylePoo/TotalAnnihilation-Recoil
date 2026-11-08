-- Feature definitions (converted from CORE_T1_BOT_Storm_dead.tdf)

return {
	core_t1_bot_storm_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_BOT_Storm_dead.s3o",
		featuredead = "CORE_T1_BOT_Storm_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 103,
		damage = 592,  -- TA 3.1c (was 145)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_bot_storm_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2c.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 52,
		damage = 592,  -- TA 3.1c (was 157)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
