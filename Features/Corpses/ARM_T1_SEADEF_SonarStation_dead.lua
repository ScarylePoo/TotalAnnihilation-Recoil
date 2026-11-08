-- Feature definitions (converted from ARM_T1_SEADEF_SonarStation_dead.tdf)

return {
	arm_t1_seadef_sonarstation_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T1_SEADEF_SonarStation_dead.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 16,
		damage = 24000,  -- TA 3.1c (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T1_SEADEF_SonarStation_heap",
	},
	arm_t1_seadef_sonarstation_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "2x2a.s3o",
		footprintx = 2,
		footprintz = 2,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 8,
		damage = 24000,  -- TA rule: = its wreck (was 36000)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
