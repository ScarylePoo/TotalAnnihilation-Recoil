-- Feature definitions (converted from CORE_T1_VEH_Leveler_dead.tdf)

return {
	core_t1_veh_leveler_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_VEH_Leveler_dead",
		featuredead = "CORE_T1_VEH_Leveler_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 116,  -- 233
		damage = 150,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_veh_leveler_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2b",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 58,  -- 116
		damage = 75,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
