-- Feature definitions (converted from CORE_T1_LAB_Shipyard_dead.tdf)

return {
	core_t1_lab_shipyard_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_LAB_Shipyard_dead.s3o",
		footprintx = 7,
		footprintz = 7,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 480,  -- TA 3.1c (was 780)
		damage = 24000,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T1_LAB_Shipyard_heap",
	},
	core_t1_lab_shipyard_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "7x7d.s3o",
		footprintx = 7,
		footprintz = 7,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 240,  -- TA rule: half of its wreck (was 390)
		damage = 24000,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
