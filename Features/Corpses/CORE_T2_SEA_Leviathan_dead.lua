-- Feature definitions (converted from CORE_T2_SEA_Leviathan_dead.tdf)

return {
	core_t2_sea_leviathan_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_SEA_Leviathan_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 1652,
		damage = 794,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T2_SEA_Leviathan_heap",
	},
	core_t2_sea_leviathan_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3c.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 826,
		damage = 794,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
