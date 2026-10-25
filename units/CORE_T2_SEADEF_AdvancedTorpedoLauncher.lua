-- CORE_T2_SEADEF_AdvancedTorpedoLauncher (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t2_seadef_advancedtorpedolauncher = {
		-- id
		name = "Advanced Torpedo Launcher",
		description = "Advanced Torpedo Launcher",
		side = "CORE",
		unitname = "core_t2_seadef_advancedtorpedolauncher",
		objectname = "CORE_T2_SEADEF_AdvancedTorpedoLauncher",
		corpse = "CORE_T2_SEADEF_AdvancedTorpedoLauncher_dead",
		icontype = "turret",
		category = "CORE SPECIAL LEVEL2 WEAPON NOTAIR",
		-- costs, makes, uses, storage
		buildcostenergy = 5389,
		buildcostmetal = 1758,
		buildtime = 6575,
		-- movement or placement
		minwaterdepth = 10,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "MEDIUM_UNIT",
		-- properties
		maxdamage = 562,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 250,
		sonardistance = 950,
		-- other abilities
		activatewhenbuilt = 1,
		-- unit animation
		waterline = 15,
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
				name = "CORATL_TORPEDO",
			},
		},
	},
}
