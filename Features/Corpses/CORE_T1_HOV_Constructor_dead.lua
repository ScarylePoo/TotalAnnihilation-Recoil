-- Feature definitions (converted from CORE_T1_HOV_Constructor_dead.tdf)

return {
	core_t1_hov_constructor_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_HOV_Constructor_dead.s3o",
		featuredead = "CORE_T1_HOV_Constructor_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 342,
		damage = 592,  -- TA 3.1c (was 550)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_hov_constructor_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4d.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 157,
		damage = 592,  -- TA rule: = its wreck (was 574)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
