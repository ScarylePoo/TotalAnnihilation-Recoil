-- ARM_T2_DEF_FortificationWall (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_fortificationwall = {
		-- id
		name = "Fortification Wall",
		description = "Perimeter Defense",
		side = "ARM",
		unitname = "arm_t2_def_fortificationwall",
		objectname = "ARM_T2_DEF_FortificationWall",
		script = "ARM_T2_DEF_FortificationWall.lua",
		corpse = "ARM_T2_DEF_FortificationWall_dead",
		category = "ARM LEVEL2 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 675,
		buildcostmetal = 27,
		buildtime = 965,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 32,
		-- properties
		maxdamage = 2000,
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
