-- Feature definitions (converted from CORE_T2_VEH_Informer_dead.tdf)

return {
	core_t2_veh_informer_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_VEH_Informer_dead.s3o",
		featuredead = "CORE_T2_VEH_Informer_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 72,
		damage = 100,  -- 400
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_veh_informer_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2f",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 36,
		damage = 97,  -- 400
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
