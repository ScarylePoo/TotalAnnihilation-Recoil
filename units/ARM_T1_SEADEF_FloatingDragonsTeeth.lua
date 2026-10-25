-- ARM_T1_SEADEF_FloatingDragonsTeeth (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seadef_floatingdragonsteeth = {
		-- id
		name = "Floating Dragon's Teeth",
		description = "Floating Dragon's Teeth",
		side = "ARM",
		unitname = "arm_t1_seadef_floatingdragonsteeth",
		objectname = "ARM_T1_SEADEF_FloatingDragonsTeeth",
		script = "ARM_T1_SEADEF_FloatingDragonsTeeth.lua",
		corpse = "ARM_T1_SEADEF_FloatingDragonsTeeth_dead",
		category = "ARM LEVEL1 NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 600,
		buildcostmetal = 20,
		buildtime = 930,
		-- movement or placement
		maxslope = 32,
		maxwaterdepth = 0,
		minwaterdepth = 1,
		-- properties
		maxdamage = 1000,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 100,
		-- other abilities
		isfeature = 1,
		-- unit animation
		waterline = 4,
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
