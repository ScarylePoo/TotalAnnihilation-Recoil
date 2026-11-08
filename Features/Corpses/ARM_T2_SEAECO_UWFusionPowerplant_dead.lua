-- Feature definitions (converted from ARM_T2_SEAECO_UWFusionPowerplant_dead.tdf)

return {
	arm_t2_seaeco_uwfusionpowerplant_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_SEAECO_UWFusionPowerplant_dead.s3o",
		featuredead = "ARM_T2_SEAECO_UWFusionPowerplant_heap",
		footprintx = 5,
		footprintz = 5,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 5668,
		damage = 985,  -- TA 3.1c (was 244)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_seaeco_uwfusionpowerplant_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "5x5c.s3o",
		footprintx = 5,
		footprintz = 5,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 2834,
		damage = 492,  -- TA 3.1c (was 122)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
