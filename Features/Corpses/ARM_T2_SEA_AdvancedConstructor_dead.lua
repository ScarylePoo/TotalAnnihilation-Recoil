-- Feature definitions (converted from ARM_T2_SEA_AdvancedConstructor_dead.tdf)

return {
	arm_t2_sea_advancedconstructor_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_SEA_AdvancedConstructor_dead.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 556,  -- TA 3.1c (was 656)
		damage = 288,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T2_SEA_AdvancedConstructor_heap",
	},
	arm_t2_sea_advancedconstructor_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3a.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 278,  -- TA rule: half of its wreck (was 328)
		damage = 288,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
