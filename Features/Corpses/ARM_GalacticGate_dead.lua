-- Feature definitions (converted from the TA armgate_dead corpse; TA named a heap it never defined, so the
-- heap here is the generic 4x4 one at half the wreck's metal, as for every other unit)

return {
	arm_galacticgate_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_GalacticGate_dead.s3o",
		featuredead = "ARM_GalacticGate_heap",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 171172,
		damage = 2301,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_galacticgate_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4b.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 85586,
		damage = 2301,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
