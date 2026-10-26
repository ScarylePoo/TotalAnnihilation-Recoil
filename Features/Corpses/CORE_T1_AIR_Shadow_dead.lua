-- Feature definitions (converted from CORE_T1_AIR_Shadow_dead.tdf)

return {
	core_t1_air_shadow_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_AIR_Shadow_dead.s3o",
		featuredead = "CORE_T1_AIR_Shadow_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 111,
		damage = 60,  -- 240
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t1_air_shadow_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3f",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 63,
		damage = 60,  -- 240
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
