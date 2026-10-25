-- Movement classes (converted from Moveinfo.TDF; the array order was the CLASSn order)

return {
	{
		name = "SMALL_SHIP",
		footprintx = 4,
		footprintz = 4,
		minwaterdepth = 5,
		-- ARM_T1_SEA_Constructor
		-- ARM_T1_SEA_Crusader
		-- ARM_T1_SEA_Skeeter
		-- ARM_T2_SEA_Archer
		-- ARM_T2_SEA_Escort
		-- CORE_T1_SEA_Constructor
		-- CORE_T1_SEA_Enforcer
		-- CORE_T1_SEA_Searcher
		-- CORE_T2_SEA_Phantom
		-- CORE_T2_SEA_Shredder
	},
	{
		name = "MEDIUM_SHIP",
		footprintx = 6,
		footprintz = 6,
		minwaterdepth = 10,
		-- ARM_T1_SEA_Hulk
		-- ARM_T2_SEA_Conqueror
		-- ARM_T2_SEA_Ranger
		-- CORE_T1_SEA_Envoy
		-- CORE_T2_SEA_Executioner
		-- CORE_T2_SEA_MissileFrigate
	},
	{
		name = "BIG_SHIP",
		footprintx = 8,
		footprintz = 8,
		minwaterdepth = 20,
		-- ARM_T2_SEA_Colossus
		-- ARM_T2_SEA_Millenium
		-- CORE_T2_SEA_Hive
		-- CORE_T2_SEA_Warlord
	},
	{
		name = "SHIP_SUBMARINE",  -- odd naming needed for spring to identify the class as sea movement
		footprintx = 3,
		footprintz = 3,
		minwaterdepth = 15,
		submarine = 1,
		-- ARM_T1_SEA_Lurker
		-- ARM_T2_SEA_AdvancedConstructor
		-- ARM_T2_SEA_Fibber
		-- ARM_T2_SEA_Piranha
		-- CORE_T1_SEA_Snake
		-- CORE_T2_SEA_AdvancedConstructor
		-- CORE_T2_SEA_Leviathan
		-- CORE_T2_SEA_Shark
	},
	{
		name = "COMMANDER",
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 400,
		maxslope = 50,
		-- ARM_Commander
		-- ARM_T2_BOT_DecoyCommander
		-- CORE_Commander
		-- CORE_T2_BOT_DecoyCommander
	},
	{
		name = "TANKSH3",
		footprintx = 3,
		footprintz = 3,
		maxwaterdepth = 20,
		maxslope = 16,
	},
	{  -- TANKS AND KBOTS USE THIS ONE
		name = "TANKSH2",
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 20,
		maxslope = 20,
	},
	{
		name = "SPID3",
		footprintx = 3,
		footprintz = 3,
		maxwaterdepth = 24,
	},
	{
		name = "TANKHOVER3",
		footprintx = 3,
		footprintz = 3,
		maxslope = 15,
		badslope = 15,
		maxwaterslope = 255,
		badwaterslope = 255,
	},
	{
		name = "KBOTSTANDARD",
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 18,
		maxslope = 36,
	},
	{
		name = "KBOTBAD",
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 16,
		maxslope = 24,  -- 32
	},
	{
		name = "KBOTGOOD",
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 20,
		maxslope = 42,
	},
	{
		name = "AMPHTANK",
		footprintx = 3,  -- 2
		footprintz = 3,  -- 2
		maxwaterdepth = 250,
		maxslope = 32,
		maxwaterslope = 455,
		crushstrength = 190,
	},
	{
		name = "KROGOTH",
		footprintx = 6,
		footprintz = 6,
		maxwaterdepth = 50,
		maxslope = 32,
		crushstrength = 1000,
	},
	{
		name = "HEAVYTANK",
		footprintx = 3,
		footprintz = 3,
		maxwaterdepth = 16,
		maxslope = 16,
		crushstrength = 250,
	},
	{
		name = "CRAWLING_BOMB",
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 200,
	},
	{
		name = "GOLIATH",
		footprintx = 3,
		footprintz = 3,
		maxwaterdepth = 16,
		maxslope = 16,
		crushstrength = 500,
	},
}
