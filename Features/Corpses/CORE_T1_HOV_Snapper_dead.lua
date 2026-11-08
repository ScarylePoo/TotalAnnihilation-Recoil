-- Feature definitions (converted from CORE_T1_HOV_Snapper_dead.tdf)

return {
	core_t1_hov_snapper_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_HOV_Snapper_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 224,
		damage = 480,  -- TA 3.1c (was 120)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T1_HOV_Snapper_heap",
	},
	core_t1_hov_snapper_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3b.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 112,
		damage = 480,  -- TA rule: = its wreck (was 120)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
