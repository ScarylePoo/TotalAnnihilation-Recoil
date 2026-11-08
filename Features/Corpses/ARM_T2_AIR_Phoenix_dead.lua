-- Feature definitions (converted from ARM_T2_AIR_Phoenix_dead.tdf)

return {
	arm_t2_air_phoenix_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_AIR_Phoenix_dead.s3o",
		featuredead = "ARM_T2_AIR_Phoenix_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 161,
		damage = 240,  -- TA 3.1c (armpnix_dead) (was 360)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_air_phoenix_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2e.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 80,
		damage = 240,  -- TA 3.1c (armpnix_heap) (was 360)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
