-- Feature definitions (converted from ARM_T2_SEADEF_AdvancedTorpedoLauncher_dead.tdf)

return {
	arm_t2_seadef_advancedtorpedolauncher_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_SEADEF_AdvancedTorpedoLauncher_dead.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 643,
		damage = 850,  -- 1160
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T2_SEADEF_AdvancedTorpedoLauncher_heap",
	},
	arm_t2_seadef_advancedtorpedolauncher_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4a.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 322,
		damage = 850,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
