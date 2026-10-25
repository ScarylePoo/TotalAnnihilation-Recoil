-- ARM_T2_SEADEF_AdvancedTorpedoLauncher (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	arm_t2_seadef_advancedtorpedolauncher = {
		-- id
		name = "Advanced Torpedo Launcher",
		description = "Advanced Torpedo Launcher",
		side = "ARM",
		unitname = "arm_t2_seadef_advancedtorpedolauncher",
		objectname = "ARM_T2_SEADEF_AdvancedTorpedoLauncher",
		script = "ARM_T2_SEADEF_AdvancedTorpedoLauncher.lua",
		corpse = "ARM_T2_SEADEF_AdvancedTorpedoLauncher_dead",
		icontype = "turret",
		category = "ARM SPECIAL LEVEL2 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 4942,
		buildcostmetal = 1762,
		buildtime = 6262,
		-- movement or placement
		minwaterdepth = 10,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "MEDIUM_UNIT",
		-- properties
		maxdamage = 520,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 260,
		sonardistance = 950,
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		waterline = 25,
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
				"torpok1",
			},
			select = {
				"torpadv2",
			},
			underattack = "warning1",
		},
		weapons = {
			{
				name = "ARMATL_TORPEDO",
			},
		},
	},
}
