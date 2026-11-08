-- Feature definitions (converted from ARM_T1_VEH_Podger_dead.tdf)

return {
	arm_t1_veh_podger_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_VEH_Podger_dead.s3o",
		featuredead = "ARM_T1_VEH_Podger_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 138,
		damage = 960,  -- TA 3.1c (was 240)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t1_veh_podger_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3b.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 69,
		damage = 480,  -- TA 3.1c (was 120)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
