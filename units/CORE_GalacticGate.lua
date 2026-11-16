-- CORE_GalacticGate (converted from the TA corgate.fbi): the campaign's Galactic Gate, a mission objective.
-- Static and inert: TA's teleporter=1 and energyuse=3000 have no meaning here, and nothing builds it.

return {
	core_galacticgate = {
		-- id
		name = "Galactic Gate",
		description = "Space Teleporter",
		side = "CORE",
		unitname = "core_galacticgate",
		objectname = "CORE_GalacticGate.s3o",
		buildpic = "CORE_GalacticGate.png",
		script = "CORE_GalacticGate.lua",
		corpse = "CORE_GalacticGate_dead",
		category = "CORE SPECIAL NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1982431,
		buildcostmetal = 197485,
		buildtime = 3421694,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "CRAWL_BLASTSML",
		-- properties
		maxdamage = 2469,
		idletime = 2200,
		idleautoheal = 0,
		sightdistance = 210,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		-- what are these? or more importantly, do they work/have meaning?
		bmcode = 0,
		threed = 1,
		zbuffer = 1,
		noautofire = 0,
		buildangle = 2048,
		ovradjust = 1,
		sounds = {
			canceldestruct = "cancel2",
			cant = {
				"cantdo4",
			},
			count = {
				[0] = "count6",
				[1] = "count5",
				[2] = "count4",
				[3] = "count3",
				[4] = "count2",
				[5] = "count1",
			},
			ok = {
				"drone1",
			},
			select = {
				"drone1",
			},
			underattack = "warning1",
		},
	},
}
