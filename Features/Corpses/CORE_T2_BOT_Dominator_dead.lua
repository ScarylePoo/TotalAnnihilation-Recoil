-- Feature definitions (converted from CORE_T2_BOT_Dominator_dead.tdf)

return {
	core_t2_bot_dominator_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_BOT_Dominator_dead",
		featuredead = "CORE_T2_BOT_Dominator_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 301,
		damage = 228,  -- 950
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_bot_dominator_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2b",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 122,
		damage = 60,  -- 240
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
