-- Feature definitions (converted from CORE_T2_SEA_MissileFrigate_dead.tdf)

return {
	core_t2_sea_missilefrigate_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_SEA_MissileFrigate_dead.s3o",
		footprintx = 6,
		footprintz = 6,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 1826,
		damage = 24000,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T2_SEA_MissileFrigate_heap",
	},
	core_t2_sea_missilefrigate_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "6x6b.s3o",
		footprintx = 6,
		footprintz = 6,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 913,
		damage = 24000,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
