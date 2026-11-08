-- Feature definitions (converted from CORE_T2_BOT_Parasite_dead.tdf)

return {
	core_t2_bot_parasite_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_BOT_Parasite_dead.s3o",
		featuredead = "CORE_T2_BOT_Parasite_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 125,
		damage = 272,  -- TA 3.1c (was 75)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_bot_parasite_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "1x1a.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 63,
		damage = 136,  -- TA 3.1c (was 52)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
