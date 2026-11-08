-- Feature definitions (converted from CORE_T2_BOT_Morty_dead.tdf)

return {
	core_t2_bot_morty_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_BOT_Morty_dead.s3o",
		featuredead = "CORE_T2_BOT_Morty_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 257,
		damage = 736,  -- TA 3.1c (was 182)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_bot_morty_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2a.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 129,
		damage = 368,  -- TA 3.1c (was 101)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
