-- CORE_T1_DEF_LightLaserTower (converted from FBI; build lists: gamedata/unitdefs_pre.lua)

return {
	core_t1_def_lightlasertower = {
		-- id
		name = "Light Laser Tower",
		description = "Light Laser Tower",
		side = "CORE",
		unitname = "core_t1_def_lightlasertower",
		objectname = "CORE_T1_DEF_LightLaserTower",
		script = "CORE_T1_DEF_LightLaserTower.lua",
		corpse = "CORE_T1_DEF_LightLaserTower_dead",
		icontype = "turret",
		category = "CORE LEVEL1 WEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1908,
		buildcostmetal = 195,
		buildtime = 4724,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		firestate = 2,
		badtargetcategory = "VTOL",
		explodeas = "MEDIUM_BUILDINGEX",
		selfdestructas = "MEDIUM_BUILDING",
		-- properties
		maxdamage = 610,
		hidedamage = 1,
		idletime = 2200,
		idleautoheal = .5,
		sightdistance = 613,
		-- unit animation
		footprintx = 2,
		footprintz = 2,
		yardmap = "oo oo",
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
		weapons = {
			{
				name = "CORE_LIGHT_LASER",
			},
		},
	},
}
