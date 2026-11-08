-- Feature definitions (converted from CORE_T2_SEADEF_AdvancedSonar_dead.tdf)

return {
	core_t2_seadef_advancedsonar_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_SEADEF_AdvancedSonar_dead.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 122,
		damage = 192,  -- TA 3.1c (was 242)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
		featuredead = "CORE_T2_SEADEF_AdvancedSonar_heap",
	},
	core_t2_seadef_advancedsonar_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "3x3e.s3o",
		footprintx = 3,
		footprintz = 3,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 61,
		damage = 192,  -- TA rule: = its wreck (was 242)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
