-- Feature definitions (converted from CORE_T2_SEADEF_AdvancedTorpedoLauncher_dead.tdf)

return {
	core_t2_seadef_advancedtorpedolauncher_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_SEADEF_AdvancedTorpedoLauncher_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 1006,
		damage = 415,  -- 450
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T2_SEADEF_AdvancedTorpedoLauncher_heap",
	},
	core_t2_seadef_advancedtorpedolauncher_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3f.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 503,
		damage = 415,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
