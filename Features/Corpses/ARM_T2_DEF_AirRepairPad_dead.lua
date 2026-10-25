-- Feature definitions (converted from ARM_T2_DEF_AirRepairPad_dead.tdf)

return {
	arm_t2_def_airrepairpad_dead = {
		world = "All Worlds",
		description = "Wreckage",
		category = "arm_corpses",
		object = "ARM_T2_DEF_AirRepairPad_dead",
		featuredead = "ARM_T2_DEF_AirRepairPad_heap",
		footprintx = 4,
		footprintz = 4,
		height = 40,
		blocking = 1,
		hitdensity = 100,
		metal = 340,
		damage = 136,  -- 544
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
	arm_t2_def_airrepairpad_heap = {
		world = "All Worlds",
		description = "Wreckage",
		category = "heaps",
		object = "4x4a",
		footprintx = 1,
		footprintz = 1,
		height = 4,
		blocking = 0,
		hitdensity = 100,
		metal = 170,
		damage = 136,  -- 544
		reclaimable = 1,
		featurereclamate = "smudge01",
		seqnamereclamate = "tree1reclamate",
	},
}
