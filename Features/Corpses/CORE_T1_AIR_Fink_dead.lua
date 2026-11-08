-- Feature definitions (converted from CORE_T1_AIR_Fink_dead.tdf)

return {
	core_t1_air_fink_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_AIR_Fink_dead.s3o",
		featuredead = "CORE_T1_AIR_Fink_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 42,
		damage = 72,  -- TA 3.1c (corfink_dead) (was 36)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_air_fink_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2d.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 21,
		damage = 72,  -- TA 3.1c (corfink_heap) (was 19)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
