-- Feature definitions (converted from CORE_T1_AIR_Constructor_dead.tdf)

return {
	core_t1_air_constructor_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_AIR_Constructor_dead.s3o",
		featuredead = "CORE_T1_AIR_Constructor_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 194,
		damage = 232,  -- TA rule: 0.8 x unit HP 290 (was 539)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_air_constructor_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2f.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 87,
		damage = 232,  -- TA rule: = its wreck (was 555)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
