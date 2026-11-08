-- Feature definitions (converted from ARM_T1_SEADEF_TorpedoLauncher_dead.tdf)

return {
	arm_t1_seadef_torpedolauncher_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_SEADEF_TorpedoLauncher_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 723,
		damage = 24000,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_SEADEF_TorpedoLauncher_heap",
	},
	arm_t1_seadef_torpedolauncher_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3d.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 362,
		damage = 24000,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
