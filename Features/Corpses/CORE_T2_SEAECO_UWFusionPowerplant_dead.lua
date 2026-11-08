-- Feature definitions (converted from CORE_T2_SEAECO_UWFusionPowerplant_dead.tdf)

return {
	core_t2_seaeco_uwfusionpowerplant_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_SEAECO_UWFusionPowerplant_dead.s3o",
		featuredead = "CORE_T2_SEAECO_UWFusionPowerplant_heap",
		footprintx = 5,
		footprintz = 5,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 5768,
		damage = 1140,  -- TA 3.1c (was 1290)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_seaeco_uwfusionpowerplant_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "5x5a.s3o",
		footprintx = 5,
		footprintz = 5,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 2884,
		damage = 570,  -- TA 3.1c (was 545)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
