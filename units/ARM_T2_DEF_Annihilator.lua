-- ARM_T2_DEF_Annihilator (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_def_annihilator = {
		-- id
		name = "Annihilator",
		description = "Long Range Energy weapon",
		side = "ARM",
		unitname = "arm_t2_def_annihilator",
		objectname = "ARM_T2_DEF_Annihilator.s3o",
		buildpic = "ARM_T2_DEF_Annihilator.png",
		script = "ARM_T2_DEF_Annihilator.lua",
		corpse = "ARM_T2_DEF_Annihilator_dead",
		category = "ARM SPECIAL WEAPON LEVEL2 NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 25025,
		buildcostmetal = 3985,
		buildtime = 75071,
		damagemodifier = 0.5,  -- TA 3.1c (was unset)
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "CRAWL_BLASTSML",
		-- properties
		maxdamage = 1410,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 380,  -- TA 3.1c (was 665)
		radardistance = 1200,  -- TA 3.1c (was 1500)
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
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
		buildangle = 4096,
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
				"anni",
			},
			select = {
				"anni",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ANNIHILATOR_BEAM",
			},
		},
	},
}
