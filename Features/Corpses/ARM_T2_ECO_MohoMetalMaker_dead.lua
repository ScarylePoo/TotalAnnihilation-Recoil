-- Feature definitions (converted from ARM_T2_ECO_MohoMetalMaker_dead.tdf)

return {
	arm_t2_eco_mohometalmaker_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "ARM_T2_ECO_MohoMetalMaker_dead.s3o",
		featuredead = "ARM_T2_ECO_MohoMetalMaker_heap",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 46,
		damage = 320,  -- TA 3.1c (was 73)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_eco_mohometalmaker_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4c.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 23,
		damage = 160,  -- TA 3.1c (was 40)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
