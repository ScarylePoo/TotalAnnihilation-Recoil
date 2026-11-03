-- Feature definitions (converted from CORE_T1_SEADEF_Stinger_dead.tdf)

return {
	core_t1_seadef_stinger_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_SEADEF_Stinger_dead.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 57,
		damage = 159,  -- 232
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T1_SEADEF_Stinger_heap",
	},
	core_t1_seadef_stinger_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4b.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 28,
		damage = 159,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
