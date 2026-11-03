-- Feature definitions (converted from ARM_T2_SEADEF_AdvancedSonar_dead.tdf)

return {
	arm_t2_seadef_advancedsonar_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_SEADEF_AdvancedSonar_dead.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 40,
		blocking = 0,
		hitdensity = 100,
		metal = 130,
		damage = 164,  -- 256
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "ARM_T2_SEADEF_AdvancedSonar_heap",
	},
	arm_t2_seadef_advancedsonar_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4c.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 65,
		damage = 164,
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
