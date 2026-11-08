-- Feature definitions (converted from ARM_T2_VEH_Phalanx_dead.tdf)

return {
	arm_t2_veh_phalanx_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_VEH_Phalanx_dead.s3o",
		featuredead = "ARM_T2_VEH_Phalanx_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 664,
		damage = 256,  -- TA 3.1c (was 63)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_veh_phalanx_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2a.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 332,
		damage = 128,  -- TA 3.1c (was 31)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
