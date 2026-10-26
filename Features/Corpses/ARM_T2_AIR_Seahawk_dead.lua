-- Feature definitions (converted from ARM_T2_AIR_Seahawk_dead.tdf)

return {
	arm_t2_air_seahawk_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_AIR_Seahawk_dead.s3o",
		featuredead = "ARM_T2_AIR_Seahawk_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 121,
		damage = 360,  -- 240
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_air_seahawk_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2e",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 59,
		damage = 360,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
