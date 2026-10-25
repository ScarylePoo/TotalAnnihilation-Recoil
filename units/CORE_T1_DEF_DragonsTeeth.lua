-- CORE_T1_DEF_DragonsTeeth (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_def_dragonsteeth = {
		-- id
		name = "Dragon's Teeth",
		description = "Perimeter Defense",
		side = "CORE",
		unitname = "core_t1_def_dragonsteeth",
		objectname = "CORE_T1_DEF_DragonsTeeth",
		script = "CORE_T1_DEF_DragonsTeeth.lua",
		corpse = "CORE_T1_DEF_DragonsTeeth_dead",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 300,
		buildcostmetal = 11,
		buildtime = 565,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 32,
		-- properties
		maxdamage = 350,
		hidedamage = 1,
		mass = 100,
		sightdistance = 100,
		-- other abilities
		isfeature = 1,
		-- unit animation
		footprintx = 2,
		footprintz = 2,
		yardmap = "oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
		ovradjust = 1,
	},
}
