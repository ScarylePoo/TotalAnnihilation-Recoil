-- Feature definitions (converted from CORE_T1_HOV_Nixer_dead.tdf)

return {
	core_t1_hov_nixer_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_HOV_Nixer_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 254,
		damage = 91,  -- 368
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T1_HOV_Nixer_heap",
	},
	core_t1_hov_nixer_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3d.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 127,
		damage = 91,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
