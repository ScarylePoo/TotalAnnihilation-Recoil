-- Feature definitions (converted from CORE_T2_BOT_Necro_dead.tdf)

return {
	core_t2_bot_necro_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_BOT_Necro_dead.s3o",
		featuredead = "CORE_T2_BOT_Necro_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 301,  -- TA rule: 0.8 x unit metal 376 (was 132)
		damage = 376,  -- TA rule: 0.8 x unit HP 470 (was 202)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_bot_necro_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2d.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 150,  -- TA rule: half of its wreck (was 66)
		damage = 376,  -- TA rule: = its wreck (was 202)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
