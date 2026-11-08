-- Feature definitions (converted from CORE_T2_AIR_Vulture_dead.tdf)

return {
	core_t2_air_vulture_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_AIR_Vulture_dead.s3o",
		featuredead = "CORE_T2_AIR_Vulture_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 135,  -- TA rule: 0.8 x unit metal 169 (was 154)
		damage = 136,  -- TA rule: 0.8 x unit HP 170 (was 600)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_air_vulture_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3d.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 68,  -- TA rule: half of its wreck (was 77)
		damage = 136,  -- TA rule: = its wreck (was 97)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
