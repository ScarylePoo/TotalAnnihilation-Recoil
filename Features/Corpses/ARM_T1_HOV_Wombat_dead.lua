-- Feature definitions (converted from ARM_T1_HOV_Wombat_dead.tdf)

return {
	arm_t1_hov_wombat_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_HOV_Wombat_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 260,
		damage = 360,  -- TA 3.1c (was 90)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_HOV_Wombat_heap",
	},
	arm_t1_hov_wombat_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3a.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 130,
		damage = 360,  -- TA rule: = its wreck (was 90)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
