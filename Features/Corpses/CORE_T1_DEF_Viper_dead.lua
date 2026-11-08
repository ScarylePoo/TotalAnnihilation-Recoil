-- Feature definitions (converted from CORE_T1_DEF_Viper_dead.tdf)

return {
	core_t1_def_viper_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_DEF_Viper_dead.s3o",
		featuredead = "CORE_T1_DEF_Viper_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 1717,  -- TA 3.1c (was 701)
		damage = 1502,  -- TA 3.1c (was 1375)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_def_viper_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2f.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 859,  -- TA 3.1c (was 344)
		damage = 751,  -- TA 3.1c (corvipe_heap) (was 780)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
