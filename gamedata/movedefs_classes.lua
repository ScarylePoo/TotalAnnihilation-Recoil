-- Movement classes (converted from TA's Moveinfo.TDF; values TA 3.1c where marked). Laid out like Splinter Faction:
-- this file defines the classes by name, gamedata/movedefs.lua fills in missing tags from movedefs_tags.lua and runs
-- movedefs_post.lua. The engine wants an array, so the map is converted at the end (sorted by name: the same order
-- on every machine).

-- Unit heat: units add "heat" to the squares they occupy and the pathfinder routes others around it, so groups
-- spread over parallel paths instead of queueing behind each other. Always on (SF: modoption "unitheat").
-- NOTE: only the legacy pathfinder (modrules pathFinderSystem = 0, HAPFS) uses heat; QTPFS ignores it.
local unitHeat = 0.0042

local flowMappingToggle = true
local allowRawMovement = true   -- move straight at the goal when nothing is in the way (SF)

-- Speed under water for every class (Splinter Faction's genericDepthmodParams): a submerged tank or kbot moves at
-- 1 / constantCoeff = half speed at any depth down to 500 (engine default: 1 / (1 + 0.1 x depth), 9 % at 100 deep).
local genericDepthmodParams = {
	minHeight      = 0,
	maxHeight      = 500,
	maxScale       = 3,
	quadraticCoeff = 0,
	linearCoeff    = 0, -- deprecates "depthMod"
	constantCoeff  = 2,
}

local moveDefs = {
	SMALL_SHIP = {
		footprintx = 4,
		footprintz = 4,
		minwaterdepth = 3,  -- TA 3.1c (was 5)
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
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	MEDIUM_SHIP = {
		footprintx = 6,
		footprintz = 6,
		minwaterdepth = 10,
		-- ARM_T1_SEA_Hulk
		-- ARM_T2_SEA_Conqueror
		-- ARM_T2_SEA_Ranger
		-- CORE_T1_SEA_Envoy
		-- CORE_T2_SEA_Executioner
		-- CORE_T2_SEA_MissileFrigate
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	BIG_SHIP = {
		footprintx = 8,
		footprintz = 8,
		minwaterdepth = 15,  -- TA 3.1c (was 20)
		-- ARM_T2_SEA_Colossus
		-- ARM_T2_SEA_Millenium
		-- CORE_T2_SEA_Hive
		-- CORE_T2_SEA_Warlord
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	SHIP_SUBMARINE = {  -- odd naming needed for spring to identify the class as sea movement
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
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	COMMANDER = {
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 400,
		maxslope = 50,
		-- ARM_Commander
		-- ARM_T2_BOT_DecoyCommander
		-- CORE_Commander
		-- CORE_T2_BOT_DecoyCommander
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	TANKSH3 = {
		footprintx = 3,
		footprintz = 3,
		maxwaterdepth = 12,  -- TA 3.1c (was 20)
		maxslope = 16,
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	TANKSH2 = {
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 12,  -- TA 3.1c (was 20)
		maxslope = 20,
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	SPID3 = {
		footprintx = 3,
		footprintz = 3,
		maxwaterdepth = 16,  -- TA 3.1c (was 24)
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	TANKHOVER3 = {
		footprintx = 3,
		footprintz = 3,
		maxslope = 15,
		badslope = 15,
		maxwaterslope = 255,
		badwaterslope = 255,
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	KBOTSTANDARD = {
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 12,  -- TA 3.1c (was 18)
		maxslope = 36,
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	KBOTBAD = {
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 12,  -- TA 3.1c (was 16)
		maxslope = 24,  -- 32
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	KBOTGOOD = {
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 20,
		maxslope = 42,
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	AMPHTANK = {
		footprintx = 3,  -- 2
		footprintz = 3,  -- 2
		maxwaterdepth = 250,
		maxslope = 32,
		maxwaterslope = 455,
		crushstrength = 190,
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	KROGOTH = {
		footprintx = 6,
		footprintz = 6,
		maxwaterdepth = 12,  -- TA 3.1c (was 50)
		maxslope = 32,
		crushstrength = 1000,
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	HEAVYTANK = {
		footprintx = 3,
		footprintz = 3,
		maxwaterdepth = 16,
		maxslope = 16,
		crushstrength = 250,
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	CRAWLING_BOMB = {
		footprintx = 2,
		footprintz = 2,
		maxwaterdepth = 200,
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
	GOLIATH = {
		footprintx = 3,
		footprintz = 3,
		maxwaterdepth = 12,  -- TA 3.1c (was 16)
		maxslope = 16,
		crushstrength = 500,
		depthmodparams = genericDepthmodParams,
		heatmod = unitHeat,
		heatmapping = true,
		allowrawmovement = allowRawMovement,
		flowmapping = flowMappingToggle,
	},
}

--------------------------------------------------------------------------------
-- convert from map format to the expected array format

local names = {}
for name in pairs(moveDefs) do names[#names + 1] = name end
table.sort(names)

local array = {}
for i, name in ipairs(names) do
	local md = moveDefs[name]
	md.name = name
	array[i] = md
end

return array
