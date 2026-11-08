-- Feature definitions (converted from CORE_T2_LAB_AdvancedAircraftPlant_dead.tdf)

return {
	core_t2_lab_advancedaircraftplant_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_LAB_AdvancedAircraftPlant_dead.s3o",
		featuredead = "CORE_T2_LAB_AdvancedAircraftPlant_heap",
		footprintx = 7,
		footprintz = 6,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 1753,  -- TA 3.1c (was 1953)
		damage = 1760,  -- TA 3.1c (was 2439)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_lab_advancedaircraftplant_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "6x6a.s3o",
		footprintx = 6,
		footprintz = 6,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 876,
		damage = 1760,  -- TA 3.1c (was 2353)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
