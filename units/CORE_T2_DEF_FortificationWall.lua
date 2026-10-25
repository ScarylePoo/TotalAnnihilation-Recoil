-- CORE_T2_DEF_FortificationWall (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_fortificationwall = {
		-- id
		name = "Fortification Wall",
		description = "Perimeter Defense",
		side = "CORE",
		unitname = "core_t2_def_fortificationwall",
		objectname = "CORE_T2_DEF_FortificationWall",
		script = "CORE_T2_DEF_FortificationWall.lua",
		corpse = "CORE_T2_DEF_FortificationWall_dead",
		category = "CORE LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 612,
		buildcostmetal = 23,
		buildtime = 810,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 32,
		-- properties
		maxdamage = 1750,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
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
		buildangle = 0,
	},
}
