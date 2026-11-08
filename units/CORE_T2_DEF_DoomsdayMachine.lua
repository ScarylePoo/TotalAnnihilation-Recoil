-- CORE_T2_DEF_DoomsdayMachine (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_def_doomsdaymachine = {
		-- id
		name = "Doomsday Machine",
		description = "Multi Turret Energy Weapon",
		side = "CORE",
		unitname = "core_t2_def_doomsdaymachine",
		objectname = "CORE_T2_DEF_DoomsdayMachine.s3o",
		buildpic = "CORE_T2_DEF_DoomsdayMachine.png",
		script = "CORE_T2_DEF_DoomsdayMachine.lua",
		corpse = "CORE_T2_DEF_DoomsdayMachine_dead",
		category = "CORE SPECIAL LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 14245,
		buildcostmetal = 2140,
		buildtime = 39276,
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
		maxdamage = 3140,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 380,  -- TA 3.1c (was 665)
		-- other abilities
		activatewhenbuilt = 1,
		onoffable = 1,
		-- unit animation
		footprintx = 3,
		footprintz = 3,
		yardmap = "ooo ooo ooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
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
				"doom",
			},
			select = {
				"doom",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "DOOMSDAY_ANNIHILATOR_BEAM",
			},
			{
				name = "CORE_LIGHT_LASER",
			},
			{
				name = "CORE_LASERH1",
			},
		},
	},
}
