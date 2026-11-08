-- Feature definitions (converted from CORE_T2_SEA_Warlord_dead.tdf)

return {
	core_t2_sea_warlord_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_SEA_Warlord_dead.s3o",
		footprintx = 6,
		footprintz = 6,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 3345,
		damage = 24000,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T2_SEA_Warlord_heap",
	},
	core_t2_sea_warlord_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "7x7d.s3o",
		footprintx = 7,
		footprintz = 7,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 1672,
		damage = 24000,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
