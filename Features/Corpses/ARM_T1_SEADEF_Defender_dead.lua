-- Feature definitions (converted from ARM_T1_SEADEF_Defender_dead.tdf)

return {
	arm_t1_seadef_defender_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_SEADEF_Defender_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 40,
		blocking = 1,
		hitdensity = 100,
		metal = 56.8,  -- TA 3.1c (was 57)
		damage = 202,  -- TA 3.1c (was 50)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_SEADEF_Defender_heap",
	},
	arm_t1_seadef_defender_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4f.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 28,
		damage = 202,  -- TA rule: = its wreck (was 50)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
