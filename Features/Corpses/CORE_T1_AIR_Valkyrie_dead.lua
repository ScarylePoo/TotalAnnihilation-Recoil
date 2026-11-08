-- Feature definitions (converted from CORE_T1_AIR_Valkyrie_dead.tdf)

return {
	core_t1_air_valkyrie_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_AIR_Valkyrie_dead.s3o",
		featuredead = "CORE_T1_AIR_Valkyrie_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 95,
		damage = 120,  -- TA 3.1c (corvalk_dead) (was 60)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_air_valkyrie_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3c.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 47,
		damage = 120,  -- TA 3.1c (corvalk_heap) (was 30)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
