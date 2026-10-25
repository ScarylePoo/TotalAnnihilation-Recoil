-- Feature definitions (converted from ARM_T1_VEH_Jeffy_dead.tdf)

return {
	arm_t1_veh_jeffy_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_VEH_Jeffy_dead",
		featuredead = "ARM_T1_VEH_Jeffy_heap",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 30,
		damage = 16,  -- 63
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t1_veh_jeffy_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2f",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 15,
		damage = 16,  -- 63
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
