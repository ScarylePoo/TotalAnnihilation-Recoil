-- Feature definitions (converted from ARM_T1_VEH_Samson_dead.tdf)

return {
	arm_t1_veh_samson_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_VEH_Samson_dead.s3o",
		featuredead = "ARM_T1_VEH_Samson_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 114,
		damage = 184,  -- 739
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t1_veh_samson_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3d",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 57,
		damage = 184,  -- 739
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
