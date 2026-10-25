-- Feature definitions (converted from CORE_T1_VEH_Instigator_dead.tdf)

return {
	core_t1_veh_instigator_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_VEH_Instigator_dead.s3o",
		featuredead = "CORE_T1_VEH_Instigator_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 88,
		damage = 130,  -- 522
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_veh_instigator_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2f",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 44,
		damage = 127,  -- 522
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
