-- Feature definitions (converted from CORE_T2_DEF_Cobra_dead.tdf)

return {
	core_t2_def_cobra_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_DEF_Cobra_dead.s3o",
		featuredead = "CORE_T2_DEF_Cobra_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 855,
		damage = 1219,  -- TA 3.1c (was 303)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_def_cobra_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3d.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 428,
		damage = 610,  -- TA 3.1c (was 152)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
