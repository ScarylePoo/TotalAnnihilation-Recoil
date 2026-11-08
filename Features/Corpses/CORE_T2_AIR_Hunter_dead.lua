-- Feature definitions (converted from CORE_T2_AIR_Hunter_dead.tdf)

return {
	core_t2_air_hunter_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_AIR_Hunter_dead.s3o",
		featuredead = "CORE_T2_AIR_Hunter_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 114,  -- TA rule: 0.8 x unit metal 142 (was 111)
		damage = 396,  -- TA rule: 0.8 x unit HP 495 (was 360)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_air_hunter_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3b.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 57,  -- TA rule: half of its wreck (was 47)
		damage = 396,  -- TA rule: = its wreck (was 60)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
