-- Feature definitions (converted from CORE_T2_VEH_Deleter_dead.tdf)

return {
	core_t2_veh_deleter_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_VEH_Deleter_dead.s3o",
		featuredead = "CORE_T2_VEH_Deleter_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 80,
		damage = 416,  -- TA 3.1c (was 103)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_veh_deleter_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3f.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 40,
		damage = 416,  -- TA 3.1c (was 101)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
