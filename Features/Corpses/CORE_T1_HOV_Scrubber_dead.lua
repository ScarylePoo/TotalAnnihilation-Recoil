-- Feature definitions (converted from CORE_T1_HOV_Scrubber_dead.tdf)

return {
	core_t1_hov_scrubber_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_HOV_Scrubber_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 58,
		damage = 160,  -- TA 3.1c (was 40)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T1_HOV_Scrubber_heap",
	},
	core_t1_hov_scrubber_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3c.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 29,
		damage = 160,  -- TA rule: = its wreck (was 40)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
