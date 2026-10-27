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
		metal = 132,
		damage = 202,  -- 794
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_bot_necro_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2d",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 66,
		damage = 202,  -- 794
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
