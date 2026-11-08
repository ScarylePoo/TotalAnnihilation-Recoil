-- Feature definitions (converted from CORE_T1_SEAPL_Voodoo_dead.tdf)

return {
	core_t1_seapl_voodoo_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_SEAPL_Voodoo_dead.s3o",
		featuredead = "CORE_T1_SEAPL_Voodoo_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 146,  -- TA rule: 0.8 x unit metal 182 (was 236)
		damage = 127,  -- TA rule: 0.8 x unit HP 159 (was 240)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_seapl_voodoo_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2e.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 73,  -- TA rule: half of its wreck (was 119)
		damage = 127,  -- TA rule: = its wreck (was 30)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
