-- ARM_T1_SEADEF_Stingray (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seadef_stingray = {
		-- id
		name = "Stingray",
		description = "Floating Heavy Laser Tower",
		side = "ARM",
		unitname = "arm_t1_seadef_stingray",
		objectname = "ARM_T1_SEADEF_Stingray",
		script = "ARM_T1_SEADEF_Stingray.lua",
		corpse = "ARM_T1_SEADEF_Stingray_dead",
		icontype = "turret",
		category = "ARM SPECIAL LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 5796,
		buildcostmetal = 524,
		buildtime = 10178,
		-- movement or placement
		minwaterdepth = 2,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1325,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 665,
		-- unit animation
		waterline = 4,
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
		defaultmissiontype = "GUARD_NOMOVE",
		buildangle = 16384,
		noshadow = 1,
		sounds = {
			arrived = {
				"kbarmstp",
			},
			canceldestruct = "cancel2",
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			ok = {
				"kbarmmov",
			},
			select = {
				"kbarmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARM_FLOATING_TOWER_HEAVY_LASER",
			},
		},
	},
}
