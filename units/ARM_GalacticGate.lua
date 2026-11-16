-- ARM_GalacticGate (converted from the TA armgate.fbi): the campaign's Galactic Gate, a mission objective.
-- Static and inert: TA's teleporter=1 and energyuse=3000 have no meaning here, and nothing builds it.

return {
	arm_galacticgate = {
		-- id
		name = "Galactic Gate",
		description = "Space Teleporter",
		side = "ARM",
		unitname = "arm_galacticgate",
		objectname = "ARM_GalacticGate.s3o",
		buildpic = "ARM_GalacticGate.png",
		script = "ARM_GalacticGate.lua",
		corpse = "ARM_GalacticGate_dead",
		category = "ARM SPECIAL NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 1865294,
		buildcostmetal = 213965,
		buildtime = 3742578,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 10,
		-- combat
		explodeas = "ATOMIC_BLAST",
		selfdestructas = "ATOMIC_BLAST",
		-- properties
		maxdamage = 2876,
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
