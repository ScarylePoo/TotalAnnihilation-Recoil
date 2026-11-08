-- Feature definitions (converted from CORE_T1_HOV_Turtle_dead.tdf)

return {
	core_t1_hov_turtle_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_HOV_Turtle_dead.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 520,
		damage = 864,  -- TA 3.1c (was 274)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T1_HOV_Turtle_heap",
	},
	core_t1_hov_turtle_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4c.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 260,
		damage = 864,  -- TA rule: = its wreck (was 274)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
