-- Feature definitions (converted from ARM_T2_VEH_AdvancedConstructor_dead.tdf)

return {
	arm_t2_veh_advancedconstructor_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_VEH_AdvancedConstructor_dead.s3o",
		featuredead = "ARM_T2_VEH_AdvancedConstructor_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 385,  -- TA 3.1c (was 585)
		damage = 964,  -- TA 3.1c (was 941)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_veh_advancedconstructor_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3a.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 192,  -- TA 3.1c (was 292)
		damage = 964,  -- TA 3.1c (was 941)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
