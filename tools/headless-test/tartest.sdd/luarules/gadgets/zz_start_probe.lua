function gadget:GetInfo()
  return { name = "Start Probe", layer = 1001, enabled = true }
end

--------------------------------------------------------------------------------
-- run.sh STARTP=<scenario>: the pregame flow of luarules/gadgets/game_spawn.lua
-- (faction choice -> placement -> spawn) with simulated players.
--
-- Team 0 is the harness's one real player: its choices go through
-- Spring.SendLuaRulesMsg from the unsynced half, as the Slate widgets send
-- them. Other teams are marked human through GG.SpawnFlow.treatAsHuman and
-- their messages go through GG.SpawnFlow.Receive (the same handler). Teams
-- left out of that are AI teams (nobody plays them).
--
--   duel   1v1, team 1 AI. Team 0 picks Core and a spot; both phases end early.
--   teams  2v2 (0,2 vs 1,3), team 3 AI. Team 2 never picks a faction (timeout:
--          random), tries team 0's spot (refused), selects another and never
--          confirms (timeout: keeps it). Team 1 tries an enemy spot (refused).
--   ffa    4 players, one per allyteam, team 3 AI. Every spot open to all.
--          Team 0 (the real player) tries the AI's spot: refused, told through
--          its private refusedSpot/refusedCount, and no rules param it can read
--          shows an opponent's claim. Team 2 tries team 1's spot (refused).
--          Both phases end early.
--   lobby  1v1, start positions chosen in the lobby (StartPosType=3), no
--          boxes: no placement phase, commanders at the script positions.
--   lobbybox  the same with start boxes: placement still runs.
--   boxes  1v1 with start boxes (StartPosType=2): the engine's ready step is
--          taken by slate_placement's GameSetup; team 0 picks a faction but
--          no spot (timeout: auto-placed); spots and spawns must be in boxes.
--------------------------------------------------------------------------------

local opt = Spring.GetModOptions() or {}
local SCEN = opt.startprobe
if not SCEN then return end

local function log(...) Spring.Echo("[HARNESS] START", ...) end

if gadgetHandler:IsSyncedCode() then

local HUMANS = { duel = {}, teams = {1, 2}, ffa = {1, 2}, boxes = {}, lobby = {}, lobbybox = {} }
local LOBBY_POS = { [0] = {1000, 1000}, [1] = {6000, 6000} }   -- StartPosX/Z in script.txt
local phaseFrames = {}
local lastPhase
local doneFrame
local fails, passes = 0, 0

local function check(ok, what, ...)
  if ok then passes = passes + 1 else fails = fails + 1 end
  log(ok and "PASS" or "FAIL", what, ...)
end

function gadget:Initialize()
  for _, t in ipairs(HUMANS[SCEN] or {}) do GG.SpawnFlow.treatAsHuman[t] = true end
end

local function send(team, msg) GG.SpawnFlow.Receive(msg, team) end
local function spotOf(i) return Spring.GetGameRulesParam("spot_" .. i .. "_x"), Spring.GetGameRulesParam("spot_" .. i .. "_z"), Spring.GetGameRulesParam("spot_" .. i .. "_at") end
local function spotsFor(allyID)
  local list = {}
  local ffa = Spring.GetGameRulesParam("isFFA") == 1
  for i = 1, Spring.GetGameRulesParam("spotCount") or 0 do
    local _, _, at = spotOf(i)
    if ffa or at == allyID then list[#list + 1] = i end
  end
  return list
end
local function ally(t) return select(6, Spring.GetTeamInfo(t, false)) end
local function claimed(t) return Spring.GetTeamRulesParam(t, "claimedSpot") end
local function free(allyID, except)
  for _, i in ipairs(spotsFor(allyID)) do
    local taken = false
    for _, t in ipairs(Spring.GetTeamList()) do
      if claimed(t) == i then taken = true end
    end
    if not taken and i ~= except then return i end
  end
end

local placed = {}   -- team -> spot index the probe expects it at

local function placementActions(f)
  -- f: frames since the placement phase began
  if SCEN == "teams" then
    if f == 20 then
      local a0 = claimed(0)
      check(a0 ~= nil and a0 > 0, "team 0 claimed a spot with SendLuaRulesMsg", a0)
      send(2, "\139" .. tostring(a0))
      check(claimed(2) ~= a0, "team 2 refused team 0's spot while others are free", claimed(2))
      local b = free(ally(2))
      send(2, "\139" .. b)
      placed[2] = b
      check(claimed(2) == b, "team 2 selected a free spot (not confirmed)", b)
      local enemy = spotsFor(ally(0))[1]
      send(1, "\139" .. enemy)
      check(claimed(1) ~= enemy, "team 1 refused a spot on the other side", claimed(1))
      local c = free(ally(1))
      send(1, "\139" .. c); send(1, "\140")
      placed[1] = c
      check(Spring.GetTeamRulesParam(1, "confirmedSpot") == c, "team 1 confirmed", c)
    end
  elseif SCEN == "ffa" then
    if f == 20 then
      check(Spring.GetGameRulesParam("isFFA") == 1, "isFFA rules param", Spring.GetGameRulesParam("isFFA"))
      local a = free(ally(1))
      send(1, "\139" .. a); send(1, "\140")
      placed[1] = a
      send(2, "\139" .. a)
      check(claimed(2) ~= a, "team 2 refused team 1's spot", claimed(2))
      check(Spring.GetTeamRulesParam(2, "refusedCount") == 1 and Spring.GetTeamRulesParam(2, "refusedSpot") == a,
            "team 2 told its try was refused", Spring.GetTeamRulesParam(2, "refusedSpot"))
      check(Spring.GetTeamRulesParam(1, "refusedCount") == nil, "team 1 told nothing")
      placed[0] = claimed(0)
      local b = free(ally(2))
      send(2, "\139" .. b); send(2, "\140")
      placed[2] = b
    end
  end
end

local function verify()
  log("phase frames", "faction@" .. tostring(phaseFrames.faction), "placement@" .. tostring(phaseFrames.placement), "done@" .. tostring(phaseFrames.done))
  local coms = {}
  for _, t in ipairs(Spring.GetTeamList()) do
    if t ~= Spring.GetGaiaTeamID() then
      local units = Spring.GetTeamUnits(t)
      local name, x, z = "none", nil, nil
      if units[1] then
        name = UnitDefs[Spring.GetUnitDefID(units[1])].name
        x, _, z = Spring.GetUnitPosition(units[1])
      end
      local spot = Spring.GetTeamRulesParam(t, "confirmedSpot")
      if SCEN == "lobby" then
        -- no spots: the lobby position stands in for the spot
        spot = 0
        Spring.SetGameRulesParam("spot_0_x", LOBBY_POS[t][1]); Spring.SetGameRulesParam("spot_0_z", LOBBY_POS[t][2])
        Spring.SetGameRulesParam("spot_0_at", ally(t))
      end
      local sx, sz, sat = spotOf(spot or 0)
      local dist = (x and sx) and math.sqrt((x - sx) ^ 2 + (z - sz) ^ 2) or -1
      local _, ms = Spring.GetTeamResources(t, "metal")
      log("team", t, "ally", ally(t), "units", #units, name, string.format("at (%.0f, %.0f)", x or -1, z or -1),
          "spot", spot, string.format("(%.0f, %.0f) owner %s", sx or -1, sz or -1, tostring(sat)), "metal storage", ms)
      check(#units == 1 and name:find("_commander$") ~= nil, "team " .. t .. " has exactly its commander", #units, name)
      check(spot ~= nil and dist >= 0 and dist < 24, "team " .. t .. " spawned on its confirmed spot", spot, string.format("%.1f", dist))
      check(sat == ally(t) or Spring.GetGameRulesParam("isFFA") == 1, "team " .. t .. "'s spot is on its side", sat)
      check(ms == 1000, "team " .. t .. " start storage 1000", ms)
      if placed[t] then check(spot == placed[t], "team " .. t .. " is at the spot the probe chose", placed[t], spot) end
      coms[#coms + 1] = { t = t, x = x, z = z, name = name }
      if (SCEN == "boxes" or SCEN == "lobbybox") and x then
        local x1, z1, x2, z2 = Spring.GetAllyTeamStartBox(ally(t))
        check(x >= x1 and x <= x2 and z >= z1 and z <= z2, "team " .. t .. " inside its start box", x1, z1, x2, z2)
      end
    end
  end
  for i = 1, #coms do
    for j = i + 1, #coms do
      local a, b = coms[i], coms[j]
      if a.x and b.x then
        check(math.sqrt((a.x - b.x) ^ 2 + (a.z - b.z) ^ 2) > 200, "teams " .. a.t .. " and " .. b.t .. " apart")
      end
    end
  end
  local n = Spring.GetGameRulesParam("spotCount") or 0
  for i = 1, n do
    local sx, sz, sat = spotOf(i)
    local synth = Spring.GetGameRulesParam("spot_" .. i .. "_synth")
    log("spot", i, string.format("(%.0f, %.0f)", sx, sz), "owner", sat, synth == 1 and "synthetic" or "map")
    if SCEN == "boxes" or SCEN == "lobbybox" then
      local x1, z1, x2, z2 = Spring.GetAllyTeamStartBox(sat)
      check(sx >= x1 and sx <= x2 and sz >= z1 and sz <= z2, "spot " .. i .. " inside its owner's box")
    end
  end

  local name = function(t) for _, c in ipairs(coms) do if c.t == t then return c.name end end end
  if SCEN == "duel" then
    check(name(0) == "core_commander", "team 0 got the faction it chose (Core)", name(0))
    check(name(1) == "core_commander", "AI team 1 got its lobby side (CORE)", name(1))
    check(phaseFrames.placement and phaseFrames.placement < 200, "faction phase ended early once all chose", phaseFrames.placement)
    check(phaseFrames.done and phaseFrames.done - phaseFrames.placement < 200, "placement ended early once all confirmed", phaseFrames.done)
  elseif SCEN == "teams" then
    check(name(0) == "arm_commander", "team 0 got Arm (SendLuaRulesMsg)", name(0))
    check(name(1) == "core_commander", "team 1 got Core (hook)", name(1))
    check(name(3) == "arm_commander", "AI team 3 got its lobby side (ARM)", name(3))
    check(phaseFrames.placement and phaseFrames.placement >= 900, "faction phase waited for team 2 to time out", phaseFrames.placement)
    check(phaseFrames.done and phaseFrames.done - phaseFrames.placement >= 900, "placement waited for team 2 to time out", phaseFrames.done)
  elseif SCEN == "ffa" then
    check(name(0) == "core_commander" and name(1) == "arm_commander" and name(2) == "core_commander", "chosen factions", name(0), name(1), name(2))
    check(phaseFrames.done and phaseFrames.done < 400, "both phases ended early", phaseFrames.done)
  elseif SCEN == "lobby" then
    check(name(0) == "arm_commander", "team 0 got Arm", name(0))
    check(phaseFrames.placement == nil, "no placement phase", phaseFrames.placement)
    check((Spring.GetGameRulesParam("spotCount") or 0) == 0, "no spots published", Spring.GetGameRulesParam("spotCount"))
  elseif SCEN == "lobbybox" then
    check(phaseFrames.placement ~= nil, "placement phase runs with start boxes", phaseFrames.placement)
  elseif SCEN == "boxes" then
    check(name(0) == "arm_commander", "team 0 got Arm", name(0))
    check(phaseFrames.done and phaseFrames.done - phaseFrames.placement >= 900, "placement waited for team 0 to time out", phaseFrames.done)
  end
  log("RESULT", fails == 0 and "PASS" or "FAIL", passes, "checks passed", fails, "failed")
end

function gadget:GameFrame(n)
  local p = Spring.GetGameRulesParam("phase")
  if p ~= lastPhase then
    phaseFrames[p or "nil"] = n
    log("phase", p, "frame", n)
    lastPhase = p
  end
  if SCEN == "teams" and n == 5 then send(1, "\138" .. UnitDefNames.core_commander.id) end
  if SCEN == "ffa" and n == 5 then
    send(1, "\138" .. UnitDefNames.arm_commander.id)
    send(2, "\138" .. UnitDefNames.core_commander.id)
    send(2, "\138" .. 99999)   -- not a commander: ignored
  end
  if p == "placement" then
    placementActions(n - phaseFrames.placement)
    if SCEN == "ffa" and n == phaseFrames.placement + 1 then
      -- tell the unsynced half (team 0) which spot the AI holds; it cannot see it
      Spring.SetGameRulesParam("probe_aispot", claimed(3) or -1)
    end
  end
  if p == "done" and not doneFrame then doneFrame = n end
  if doneFrame and n == doneFrame + 5 then verify() end
  if not doneFrame and n == 2400 then log("FAIL", "never reached phase done"); log("RESULT", "FAIL") ; doneFrame = n - 10 end
end

else -- unsynced: team 0, the real player, as the widgets would

local FACTION = { duel = "core_commander", teams = "arm_commander", ffa = "core_commander", boxes = "arm_commander", lobby = "arm_commander", lobbybox = "arm_commander" }
local function ulog(ok, what, ...) Spring.Echo("[HARNESS] START", ok and "PASS" or "FAIL", what, ...) end
local placementStart

function gadget:GameFrame(n)
  if n == 3 then
    Spring.SendLuaRulesMsg("\138" .. UnitDefNames[FACTION[SCEN]].id)
  end
  local p = Spring.GetGameRulesParam("phase")
  if p == "placement" and not placementStart then placementStart = n end
  if placementStart and SCEN == "ffa" then
    -- team 0 tries the AI's spot first
    local f = n - placementStart
    local me = Spring.GetMyTeamID()
    local a = Spring.GetGameRulesParam("probe_aispot")
    if f == 5 then
      -- (whether team 0 can see the AI's claim is checked from LuaUI, in
      -- zz_harness_probe.lua: LuaRules unsynced reads everything)
      ulog(a and a > 0, "the AI holds a spot", a)
      Spring.SendLuaRulesMsg("\139" .. a)
    elseif f == 9 then
      ulog(Spring.GetTeamRulesParam(me, "refusedCount") == 1 and Spring.GetTeamRulesParam(me, "refusedSpot") == a,
           "team 0 told the AI's spot is taken", Spring.GetTeamRulesParam(me, "refusedSpot"))
      ulog(Spring.GetTeamRulesParam(me, "claimedSpot") ~= a, "team 0 did not get the AI's spot", Spring.GetTeamRulesParam(me, "claimedSpot"))
      Spring.SendLuaRulesMsg("\139" .. (a == 1 and 2 or 1))
    elseif f == 13 then
      Spring.SendLuaRulesMsg("\140")
    end
  elseif placementStart and SCEN ~= "boxes" and SCEN ~= "lobbybox" then
    local f = n - placementStart
    local myAlly = Spring.GetMyAllyTeamID()
    if f == 5 then
      local ffa = Spring.GetGameRulesParam("isFFA") == 1
      for i = 1, Spring.GetGameRulesParam("spotCount") or 0 do
        local taken = false
        for _, t in ipairs(Spring.GetTeamList()) do
          if Spring.GetTeamRulesParam(t, "claimedSpot") == i then taken = true end
        end
        if (ffa or Spring.GetGameRulesParam("spot_" .. i .. "_at") == myAlly) and not taken then
          Spring.SendLuaRulesMsg("\139" .. i)
          break
        end
      end
    elseif f == 10 then
      Spring.SendLuaRulesMsg("\140")
    end
  end
end

local quitAt
function gadget:Update()
  local n = Spring.GetGameFrame()
  if not quitAt and Spring.GetGameRulesParam("phase") == "done" then quitAt = n + 30 end
  if n >= 2500 or (quitAt and n >= quitAt) then Spring.SendCommands("quitforce") end
end

end
