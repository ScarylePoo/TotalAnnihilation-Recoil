-- Feature definitions (converted from CORE_T2_BOT_Voyeur_dead.tdf)

return {
	core_t2_bot_voyeur_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_BOT_Voyeur_dead.s3o",
		featuredead = "CORE_T2_BOT_Voyeur_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 74,
		damage = 280,  -- TA 3.1c (was 67)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_bot_voyeur_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2a.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 37,
		damage = 140,  -- TA 3.1c (was 33)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
