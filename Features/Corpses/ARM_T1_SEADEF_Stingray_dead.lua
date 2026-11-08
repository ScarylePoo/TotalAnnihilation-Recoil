-- Feature definitions (converted from ARM_T1_SEADEF_Stingray_dead.tdf)

return {
	arm_t1_seadef_stingray_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_SEADEF_Stingray_dead.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 446,
		damage = 1108,  -- TA 3.1c (was 285)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_SEADEF_Stingray_heap",
	},
	arm_t1_seadef_stingray_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4f.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 223,
		damage = 1108,  -- TA rule: = its wreck (was 285)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
