-- Feature definitions (converted from ARM_T2_LAB_AdvancedShipyard_dead.tdf)

return {
	arm_t2_lab_advancedshipyard_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_LAB_AdvancedShipyard_dead.s3o",
		featuredead = "ARM_T2_LAB_AdvancedShipyard_heap",
		footprintx = 7,
		footprintz = 7,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 2019,  -- TA 3.1c (was 2219)
		damage = 24000,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_lab_advancedshipyard_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "7x7a.s3o",
		footprintx = 5,
		footprintz = 5,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 1010,  -- TA rule: half of its wreck (was 903)
		damage = 24000,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
