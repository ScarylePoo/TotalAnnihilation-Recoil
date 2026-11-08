-- Feature definitions (converted from CORE_T2_DEF_Silencer_dead.tdf)

return {
	core_t2_def_silencer_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_DEF_Silencer_dead.s3o",
		featuredead = "CORE_T2_DEF_Silencer_heap",
		footprintx = 6,
		footprintz = 7,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 780,  -- TA 3.1c (was 2480)
		damage = 2048,  -- TA 3.1c (was 2511)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_def_silencer_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "6x6a.s3o",
		footprintx = 6,
		footprintz = 6,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 390,  -- TA 3.1c (was 1160)
		damage = 2048,  -- TA 3.1c (was 2541)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
