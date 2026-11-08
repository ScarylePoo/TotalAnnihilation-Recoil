-- Feature definitions (converted from CORE_T2_VEH_Goliath_dead.tdf)

return {
	core_t2_veh_goliath_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_VEH_Goliath_dead.s3o",
		featuredead = "CORE_T2_VEH_Goliath_heap",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 558,
		damage = 482,  -- TA 3.1c (was 2000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_veh_goliath_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4c.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 279,
		damage = 482,  -- TA 3.1c (was 1200)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
