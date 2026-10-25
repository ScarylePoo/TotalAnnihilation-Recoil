-- CORE_T1_SEADEF_FloatingDragonsTeeth (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seadef_floatingdragonsteeth = {
		-- id
		name = "Floating Dragon's Teeth",
		description = "Floating Dragon's Teeth",
		side = "CORE",
		unitname = "core_t1_seadef_floatingdragonsteeth",
		objectname = "CORE_T1_SEADEF_FloatingDragonsTeeth",
		script = "CORE_T1_SEADEF_FloatingDragonsTeeth.lua",
		corpse = "CORE_T1_SEADEF_FloatingDragonsTeeth_dead",
		category = "CORE LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 630,
		buildcostmetal = 18,
		buildtime = 1000,
		-- movement or placement
		maxwaterdepth = 0,
		minwaterdepth = 1,
		maxslope = 32,
		-- properties
		maxdamage = 1000,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 100,
		-- other abilities
		isfeature = 1,
		-- unit animation
		waterline = 16,
		footprintx = 2,
		footprintz = 2,
		yardmap = "oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 8192,
	},
}
