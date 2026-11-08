-- Feature definitions (converted from ARM_T2_DEF_TargetingFacility_dead.tdf)

return {
	arm_t2_def_targetingfacility_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_DEF_TargetingFacility_dead.s3o",
		featuredead = "ARM_T2_DEF_TargetingFacility_heap",
		footprintx = 5,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 12104,  -- TA 3.1c (was 2904)
		damage = 1160,  -- TA 3.1c (was 2293)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_def_targetingfacility_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4a.s3o",
		footprintx = 5,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 6052,  -- TA 3.1c (was 1452)
		damage = 580,  -- TA 3.1c (was 1157)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
