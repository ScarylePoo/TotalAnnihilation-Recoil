-- SURVIVAL_Beacon: the Survival AI's spawn beacon (luarules/gadgets/ai_survival.lua). The Survival AI team starts with
-- one in place of a commander and seeds a network of them; its waves come out of them, and the team is out when the last
-- one dies (customparams.iscommander: the commander-ends rules count it). It is the Core Galactic Gate's model and
-- script: a gate the invasion comes through. Nothing builds it.

return {
	survival_beacon = {
		-- id
		name = "Spawn Beacon",
		description = "Survival AI gate: waves come through it. Destroy them all to win",
		unitname = "survival_beacon",
		objectname = "CORE_GalacticGate.s3o",
		buildpic = "CORE_GalacticGate.png",
		script = "CORE_GalacticGate.lua",
		icontype = "building_gate_x14",
		category = "CORE SPECIAL NOWEAPON NOTAIR NOTSUB",
		-- costs, makes, uses, storage
		buildcostenergy = 25000,
		buildcostmetal = 4000,
		buildtime = 100000,
		-- movement or placement
		maxwaterdepth = 0,
		maxslope = 20,
		levelground = false,
		-- combat
		explodeas = "LARGE_BUILDINGEX",
		selfdestructas = "LARGE_BUILDINGEX",
		canselfdestruct = false,
		capturable = false,
		reclaimable = false,
		-- properties
		maxdamage = 9000,
		idletime = 900,
		idleautoheal = 10,
		autoheal = 5,
		sightdistance = 300,
		-- unit animation
		footprintx = 4,
		footprintz = 4,
		yardmap = "oooo oooo oooo oooo",
		customparams = {
			buildcategory = "defense",
			iscommander = 1,
		},
		sounds = {
			canceldestruct = "cancel2",
			underattack = "warning1",
			ok = { "drone1" },
			select = { "drone1" },
		},
	},
}
