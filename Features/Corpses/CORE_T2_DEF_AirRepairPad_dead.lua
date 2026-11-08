-- Feature definitions (converted from CORE_T2_DEF_AirRepairPad_dead.tdf)

return {
	core_t2_def_airrepairpad_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "core_corpses",
		object = "CORE_T2_DEF_AirRepairPad_dead.s3o",
		featuredead = "CORE_T2_DEF_AirRepairPad_heap",
		footprintx = 4,
		footprintz = 4,
		height = 20,
		blocking = 1,
		hitdensity = 100,
		metal = 344,
		damage = 552,  -- TA 3.1c (was 138)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	core_t2_def_airrepairpad_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4c.s3o",
		footprintx = 4,
		footprintz = 4,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 172,
		damage = 552,  -- TA 3.1c (was 152)
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
