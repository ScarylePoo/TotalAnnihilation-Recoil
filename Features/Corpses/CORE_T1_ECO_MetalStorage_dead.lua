-- Feature definitions (converted from CORE_T1_ECO_MetalStorage_dead.tdf)

return {
	core_t1_eco_metalstorage_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_ECO_MetalStorage_dead.s3o",
		featuredead = "CORE_T1_ECO_MetalStorage_heap",
		footprintx = 5,
		footprintz = 5,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 256,
		damage = 1045,  -- TA 3.1c (was 261)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_eco_metalstorage_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "5x5a.s3o",
		footprintx = 5,
		footprintz = 5,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 128,
		damage = 1045,  -- TA 3.1c (was 254)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
