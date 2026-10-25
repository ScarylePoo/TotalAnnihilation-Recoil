-- Feature definitions (converted from CORE_T2_VEH_Pillager_dead.tdf)

return {
	core_t2_veh_pillager_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_VEH_Pillager_dead",
		featuredead = "CORE_T2_VEH_Pillager_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 201,
		damage = 220,  -- 480
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_veh_pillager_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2b",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 100,
		damage = 220,  -- 480
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
