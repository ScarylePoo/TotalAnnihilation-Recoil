-- CORE_T1_SEADEF_TorpedoLauncher (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_seadef_torpedolauncher = {
		-- id
		name = "Torpedo Launcher",
		description = "Torpedo Launcher",
		side = "CORE",
		unitname = "core_t1_seadef_torpedolauncher",
		objectname = "CORE_T1_SEADEF_TorpedoLauncher",
		corpse = "CORE_T1_SEADEF_TorpedoLauncher_dead",
		icontype = "turret",
		category = "CORE SPECIAL LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 3058,
		buildcostmetal = 831,
		buildtime = 4233,
		-- movement or placement
		minwaterdepth = 1,
		maxslope = 10,
		-- combat
		firestate = 2,
		explodeas = "BIG_UNITEX",
		selfdestructas = "BIG_UNIT",
		-- properties
		maxdamage = 1520,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 263,
		sonardistance = 770,
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
		buildangle = 16384,
		noshadow = 1,
		ovradjust = 1,
		sounds = {
			arrived = {
				"shcorstp",
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
				"shcormov",
			},
			select = {
				"shcorsel",
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
