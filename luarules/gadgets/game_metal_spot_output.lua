function gadget:GetInfo()
	return {
		name    = "Metal Spot Output",
		desc    = "Mexes are metal makers in disguise: metalSpot_value x their multiplier, TA energy upkeep, while on",
		author  = "Scary le Poo (from Splinter Faction's Metal Maker Income Scaler)",
		date    = "2026-11-08",
		license = "GNU GPL, v2 or later",
		layer   = 0,
		enabled = true,
	}
end

--------------------------------------------------------------------------------
-- Mex unit defs (gamedata/alldefs_post.lua) extract nothing; this gadget gives a finished mex
--   metal  = metalSpot_value (game_metal_spots.lua) x customparams.metal_spot_mult (mex 1, moho 3)
--   energy = customparams.mex_energy (TA's energy use of that mex)
-- through Spring.SetUnitResourcing ("cmm" constant metal make, "cue" constant energy use), and nothing while it is
-- switched off, so TA's on/off still saves energy. Unit rules params "mex_metal" / "mex_energy" (public) say what a
-- mex makes, for widgets.
--------------------------------------------------------------------------------

if not gadgetHandler:IsSyncedCode() then
	return
end

local SetUnitResourcing  = Spring.SetUnitResourcing
local SetUnitRulesParam  = Spring.SetUnitRulesParam
local GetUnitIsActive    = Spring.GetUnitIsActive
local GetUnitHealth      = Spring.GetUnitHealth

local mexDefs = {}
for unitDefID, ud in pairs(UnitDefs) do
	local cp = ud.customParams or {}
	if cp.metal_spot_mult then
		mexDefs[unitDefID] = { mult = tonumber(cp.metal_spot_mult) or 1, energy = tonumber(cp.mex_energy) or 0 }
	end
end

local mexes = {}        -- unitID -> { def, on }
local spotValue = 0

local function Apply(unitID, m, on)
	m.on = on
	local metal = on and spotValue * m.def.mult or 0
	local energy = on and m.def.energy or 0
	SetUnitResourcing(unitID, "cmm", metal)
	SetUnitResourcing(unitID, "cue", energy)
	SetUnitRulesParam(unitID, "mex_metal", metal, { public = true })
	SetUnitRulesParam(unitID, "mex_energy", energy, { public = true })
	-- the TA mex scripts spin their arms from ExtractionRateChanged(income), which the engine only calls for real
	-- extractors: call it with half the output (a 2-metal mex spins at 1, the scripts' default; a moho faster)
	if on and metal > 0 then
		local env = Spring.UnitScript.GetScriptEnv(unitID)
		local fn = env and env.script and env.script.ExtractionRateChanged
		if fn then
			Spring.UnitScript.CallAsUnit(unitID, fn, metal * 0.5)
		end
	end
end

function gadget:UnitFinished(unitID, unitDefID)
	local def = mexDefs[unitDefID]
	if def then
		local m = { def = def }
		mexes[unitID] = m
		Apply(unitID, m, GetUnitIsActive(unitID) and true or false)
	end
end

function gadget:UnitDestroyed(unitID)
	mexes[unitID] = nil
end

function gadget:GameFrame(n)
	if n % 15 ~= 0 then
		return
	end
	local v = Spring.GetGameRulesParam("metalSpot_value") or 0
	local changed = v ~= spotValue
	spotValue = v
	for unitID, m in pairs(mexes) do
		local on = GetUnitIsActive(unitID) and true or false
		if changed or on ~= m.on then
			Apply(unitID, m, on)
		end
	end
end

function gadget:Initialize()
	spotValue = Spring.GetGameRulesParam("metalSpot_value") or 0
	for _, unitID in ipairs(Spring.GetAllUnits()) do
		local _, _, _, _, build = GetUnitHealth(unitID)
		if build and build >= 1 then
			gadget:UnitFinished(unitID, Spring.GetUnitDefID(unitID))
		end
	end
end
