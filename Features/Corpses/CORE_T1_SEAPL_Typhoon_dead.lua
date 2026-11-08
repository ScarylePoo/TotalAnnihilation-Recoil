-- Feature definitions (converted from CORE_T1_SEAPL_Typhoon_dead.tdf)

return {
	core_t1_seapl_typhoon_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_SEAPL_Typhoon_dead.s3o",
		featuredead = "CORE_T1_SEAPL_Typhoon_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 296,
		damage = 168,  -- TA rule: 0.8 x unit HP 210 (was 240)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_seapl_typhoon_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2e.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 133,
		damage = 168,  -- TA rule: = its wreck (was 30)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
