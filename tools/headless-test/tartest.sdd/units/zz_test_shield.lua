-- TEST ONLY (probe mod): an LLT with a 200-radius shield, to check the shield visuals (TA has no shields).
-- ARM_T1_DEF_LLT (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	zz_test_shield = {
		-- id
		name = "Test Shield",
		description = "Light Laser Tower",
		side = "ARM",
		unitname = "zz_test_shield",
		objectname = "ARM_T1_DEF_LLT.s3o",
		buildpic = "ARM_T1_DEF_LLT.png",
		script = "ARM_T1_DEF_LLT.lua",
		corpse = "ARM_T1_DEF_LLT_dead",
		icontype = "defense_light_t1",
		category = "ARM LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2546,  -- TA 3.1c (was 1946)
		buildcostmetal = 262,  -- TA 3.1c (was 190)
		buildtime = 4662,
		energystorage = 100,  -- TA 3.1c (was unset)
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 14,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "MEDIUM_BUILDINGEX",
		selfdestructas = "MEDIUM_BUILDING",
		-- properties
		maxdamage = 750,  -- TA 3.1c (was 550)
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 380,  -- TA 3.1c (was 665)
		-- unit animation
		footprintx = 2,
		footprintz = 2,
		yardmap = "oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
		defaultmissiontype = "GUARD_NOMOVE",
		buildangle = 32768,
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
				"servmed2",
			},
			select = {
				"servmed2",
			},
			underattack = "warning1",
		},
		customparams = { shield_radius = 200 },
		weapons = {
			{ def = "ZZ_TEST_SHIELD" },
		},
		weapondefs = {
			zz_test_shield = {
				name = "Test Shield",
				weapontype = "Shield",
				damage = { default = 10 },
				shield = {
					power = 3000, powerregen = 60, powerregenenergy = 0, radius = 200,
					startingpower = 3000, smart = true, repulser = false, visible = false,
					intercepttype = 1023,
				},
			},
		},
	},
}
