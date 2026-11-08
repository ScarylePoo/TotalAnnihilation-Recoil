-- Feature definitions (converted from ARM_T2_AIR_Eagle_dead.tdf)

return {
	arm_t2_air_eagle_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_AIR_Eagle_dead.s3o",
		featuredead = "ARM_T2_AIR_Eagle_heap",
		footprintx = 3,
		footprintz = 3,
		height = 40,
		blocking = 1,
		hitdensity = 100,
		metal = 132,  -- TA rule: 0.8 x unit metal 165 (was 127)
		damage = 88,  -- TA rule: 0.8 x unit HP 110 (was 240)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_air_eagle_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3d.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 66,  -- TA rule: half of its wreck (was 64)
		damage = 88,  -- TA rule: = its wreck (was 720)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
