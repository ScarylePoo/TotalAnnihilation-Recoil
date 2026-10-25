-- Feature definitions (converted from ARM_T1_ECO_MetalMaker_dead.tdf)

return {
	arm_t1_eco_metalmaker_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_ECO_MetalMaker_dead",
		featuredead = "ARM_T1_ECO_MetalMaker_heap",
		featurereclamate = "smudge01",
		footprintx = 3,
		footprintz = 3,
		height = 40,
		blocking = 1,
		hitdensity = 100,
		metal = 0,
		damage = 28,  -- 115
		reclaimable = 1,
		seqnamereclamate = "tree1reclamate",
	},
	arm_t1_eco_metalmaker_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3d",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 0,
		damage = 28,  -- 115
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
