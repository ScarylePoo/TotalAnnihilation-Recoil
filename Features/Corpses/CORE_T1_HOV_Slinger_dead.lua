-- Feature definitions (converted from CORE_T1_HOV_Slinger_dead.tdf)

return {
	core_t1_hov_slinger_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_HOV_Slinger_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 92,
		damage = 83,  -- 316
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T1_HOV_Slinger_heap",
	},
	core_t1_hov_slinger_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3e.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 46,
		damage = 83,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
