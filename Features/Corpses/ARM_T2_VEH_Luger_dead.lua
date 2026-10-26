-- Feature definitions (converted from ARM_T2_VEH_Luger_dead.tdf)

return {
	arm_t2_veh_luger_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_VEH_Luger_dead.s3o",
		featuredead = "ARM_T2_VEH_Luger_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 211,
		damage = 105,  -- 420
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_veh_luger_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2e",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 106,
		damage = 105,  -- 420
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
