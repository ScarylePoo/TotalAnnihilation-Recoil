-- ARM_T2_DEF_Protector (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_protector = {
		-- id
		name = "Protector",
		description = "Anti Missile Defense System",
		side = "ARM",
		unitname = "arm_t2_def_protector",
		objectname = "ARM_T2_DEF_Protector",
		corpse = "ARM_T2_DEF_Protector_dead",
		icontype = "nuke",
		category = "ARM SPECIAL LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 88124,
		buildcostmetal = 1637,
		buildtime = 55678,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL NOTAIR",
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "CRAWL_BLASTEX",
		-- properties
		maxdamage = 1180,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 155,
		-- other abilities
		damagemodifier = 0.4,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 1,
		shootme = 1,
		buildangle = 4096,
		antiweapons = 1,
		ovradjust = 1,
		sounds = {
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
				"loadwtr2",
			},
			select = {
				"loadwtr2",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ANTI_NUCLEAR_MISSILE",
			},
		},
	},
}
