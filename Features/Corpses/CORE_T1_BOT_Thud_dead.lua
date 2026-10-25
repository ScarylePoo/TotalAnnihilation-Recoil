-- Feature definitions (converted from CORE_T1_BOT_Thud_dead.tdf)

return {
	core_t1_bot_thud_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_BOT_Thud_dead.s3o",
		featuredead = "CORE_T1_BOT_Thud_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 118,
		damage = 159,  -- 640
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_bot_thud_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2d",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 59,
		damage = 156,  -- 640
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
