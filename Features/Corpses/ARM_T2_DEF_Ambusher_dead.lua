-- Feature definitions (converted from ARM_T2_DEF_Ambusher_dead.tdf)

return {
	arm_t2_def_ambusher_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_DEF_Ambusher_dead1.s3o",
		featuredead = "ARM_T2_DEF_Ambusher_dead2",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 1602,
		damage = 1326,  -- TA 3.1c (was 280)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_def_ambusher_dead2 = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_DEF_Ambusher_dead2.s3o",
		featuredead = "ARM_T2_DEF_Ambusher_heap",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 801,
		damage = 663,  -- TA 3.1c (was 160)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_def_ambusher_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3b.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 496,
		damage = 663,  -- TA rule: = its wreck (was 160)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
