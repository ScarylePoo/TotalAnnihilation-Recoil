-- ARM_T1_SEADEF_TorpedoLauncher (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t1_seadef_torpedolauncher = {
		-- id
		name = "Torpedo Launcher",
		description = "Torpedo Launcher",
		side = "ARM",
		unitname = "arm_t1_seadef_torpedolauncher",
		objectname = "ARM_T1_SEADEF_TorpedoLauncher.s3o",
		buildpic = "ARM_T1_SEADEF_TorpedoLauncher.png",
		script = "ARM_T1_SEADEF_TorpedoLauncher.lua",
		corpse = "ARM_T1_SEADEF_TorpedoLauncher_dead",
		category = "ARM SPECIAL LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 2658,
		buildcostmetal = 804,
		buildtime = 4120,
		-- movement or placement
		minwaterdepth = 1,
		-- combat
		firestate = 2,
		explodeas = "SMALL_UNITEX",
		selfdestructas = "SMALL_UNIT",
		-- properties
		maxdamage = 1450,
		idletime = 2200,
		idleautoheal = 0,  -- TA 3.1c: no idle regeneration (was .5)
		sightdistance = 150,  -- TA 3.1c (was 263)
		sonardistance = 450,  -- TA 3.1c (was 650)
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		waterline = 23,
		footprintx = 3,
		footprintz = 3,
		yardmap = "www www www",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		shootme = 1,
		defaultmissiontype = "GUARD_NOMOVE",
		buildangle = 16384,
		noshadow = 1,
		ovradjust = 1,
		sounds = {
			arrived = {
				"sharmstp",
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
				"sharmmov",
			},
			select = {
				"sharmsel",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "COAX_TORPEDO",
			},
		},
	},
}
