-- Feature definitions (converted from CORE_T2_BOT_Gimp_dead.tdf)

return {
	core_t2_bot_gimp_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_BOT_Gimp_dead.s3o",
		featuredead = "CORE_T2_BOT_Gimp_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 227,
		damage = 656,  -- TA 3.1c (was 159)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_bot_gimp_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2d.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 114,
		damage = 328,  -- TA 3.1c (was 75)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
