-- Feature definitions (converted from CORE_T1_ECO_MetalMaker_dead.tdf)

return {
	core_t1_eco_metalmaker_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_ECO_MetalMaker_dead",
		featuredead = "CORE_T1_ECO_MetalMaker_heap",
		footprintx = 4,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 0,
		damage = 30,  -- 120
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_eco_metalmaker_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3d",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 0,
		damage = 30,  -- 120
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
