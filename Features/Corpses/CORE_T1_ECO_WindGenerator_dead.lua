-- Feature definitions (converted from CORE_T1_ECO_WindGenerator_dead.tdf)

return {
	core_t1_eco_windgenerator_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_ECO_WindGenerator_dead.s3o",
		featuredead = "CORE_T1_ECO_WindGenerator_heap",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 44,
		damage = 1430,  -- TA 3.1c (was 357)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_eco_windgenerator_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4a.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 22,
		damage = 1430,  -- TA 3.1c (was 338)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
