-- Feature definitions (converted from ARM_T2_VEH_Jammer_dead.tdf)

return {
	arm_t2_veh_jammer_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_VEH_Jammer_dead.s3o",
		featuredead = "ARM_T2_VEH_Jammer_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 78,
		damage = 91,  -- 368
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_veh_jammer_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3b",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 39,
		damage = 91,  -- 368
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
