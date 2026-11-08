-- Feature definitions (converted from CORE_T1_SEADEF_TorpedoLauncher_dead.tdf)

return {
	core_t1_seadef_torpedolauncher_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T1_SEADEF_TorpedoLauncher_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 745,
		damage = 24000,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T1_SEADEF_TorpedoLauncher_heap",
	},
	core_t1_seadef_torpedolauncher_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3f.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 372,
		damage = 24000,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
