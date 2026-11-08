-- Feature definitions (converted from ARM_T2_VEH_Panther_dead.tdf)

return {
	arm_t2_veh_panther_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_VEH_Panther_dead.s3o",
		featuredead = "ARM_T2_VEH_Panther_heap",
		footprintx = 2,
		footprintz = 2,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 262,
		damage = 794,  -- TA 3.1c (was 192)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_veh_panther_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2d.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 66,
		damage = 794,  -- TA 3.1c (was 192)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
