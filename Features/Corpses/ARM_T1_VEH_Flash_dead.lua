-- Feature definitions (converted from ARM_T1_VEH_Flash_dead.tdf)

return {
	arm_t1_veh_flash_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_VEH_Flash_dead.s3o",
		featuredead = "ARM_T1_VEH_Flash_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 85,
		damage = 124,  -- 500
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t1_veh_flash_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2c",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 43,
		damage = 124,  -- 500
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
