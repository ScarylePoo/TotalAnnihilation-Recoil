-- Feature definitions (converted from CORE_T2_ECO_MohoMetalMaker_dead.tdf)

return {
	core_t2_eco_mohometalmaker_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_ECO_MohoMetalMaker_dead.s3o",
		featuredead = "CORE_T2_ECO_MohoMetalMaker_heap",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 41,
		damage = 400,  -- TA 3.1c (was 96)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_eco_mohometalmaker_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4a.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 21,
		damage = 200,  -- TA 3.1c (was 53)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
