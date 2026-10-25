-- Feature definitions (converted from CORE_T1_VEH_Spoiler_dead.tdf)

return {
	core_t1_veh_spoiler_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_VEH_Spoiler_dead.s3o",
		featuredead = "CORE_T1_VEH_Spoiler_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 75,  -- 150
		damage = 287,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_veh_spoiler_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3f",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 38,  -- 75
		damage = 98,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
