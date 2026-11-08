-- Feature definitions (converted from ARM_T2_AIR_AdvancedConstructor_dead.tdf)

return {
	arm_t2_air_advancedconstructor_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_AIR_AdvancedConstructor_dead.s3o",
		featuredead = "ARM_T2_AIR_AdvancedConstructor_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 176,  -- TA 3.1c (was 576)
		damage = 288,  -- TA 3.1c (armaca_dead) (was 272)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_air_advancedconstructor_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2a.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 88,  -- TA 3.1c (was 288)
		damage = 288,  -- TA 3.1c (armaca_heap) (was 272)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
