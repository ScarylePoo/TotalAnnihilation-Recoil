-- Feature definitions (converted from ARM_T1_HOV_Skimmer_dead.tdf)

return {
	arm_t1_hov_skimmer_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_HOV_Skimmer_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 61,
		damage = 38,  -- 160
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_HOV_Skimmer_heap",
	},
	arm_t1_hov_skimmer_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3e.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 30,
		damage = 38,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
