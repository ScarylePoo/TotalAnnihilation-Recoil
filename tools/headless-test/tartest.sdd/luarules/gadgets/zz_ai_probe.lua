function gadget:GetInfo()
  return { name = "AI Probe", layer = 1007, enabled = true }
end

-- Watches Lua AI teams play (AIPROBE=1 run.sh: team 1, and team 0 with AIBOTH=1, are Lua AIs). Runs the game as fast
-- as the engine allows, every 1800 frames echoes one [AIPROBE] line per team (units by class, resources, kills,
-- losses), and quits after modoption aiprobe frames. The AI's own decision traces come from aitrace=1 (core gadget).
local opt = Spring.GetModOptions() or {}
local LIMIT = tonumber(opt.aiprobe)
if not LIMIT then return end

if gadgetHandler:IsSyncedCode() then

local kills, losses, comDeaths = {}, {}, {}
local built = {}   -- [teamID] = { [class] = finished units }
local gaia = Spring.GetGaiaTeamID()

local function Class(ud)
  if ud.customParams and ud.customParams.iscommander then return "com" end
  if ud.isFactory then return "fac" end
  if ud.isBuilder and ud.canMove then return "con" end
  if ud.extractsMetal > 0 or (ud.customParams and ud.customParams.metal_spot_mult) then return "mex" end
  if ud.isBuilding and #ud.weapons > 0 then return "def" end
  if ud.isBuilding then return "bld" end
  if ud.canFly then return "air" end
  if #ud.weapons > 0 then return "army" end
  return "other"
end

function gadget:GameFrame(n)
  if n == 2 then
    Spring.SendCommands("cheat 1", "setmaxspeed 60", "setspeed 60")
  end
  if n == 60 then
    -- metal spot diagnostic: can each side's basic mex go on the spots nearest its commander?
    local spots = GG.metalMakerSpots or {}
    Spring.Echo("[AIPROBE] metal spots: " .. #spots)
    for _, teamID in ipairs(Spring.GetTeamList()) do
      for _, uid in ipairs(Spring.GetTeamUnits(teamID)) do
        local ud = UnitDefs[Spring.GetUnitDefID(uid)]
        if ud and ud.customParams and ud.customParams.iscommander then
          local x, _, z = Spring.GetUnitPosition(uid)
          local side = ud.name:match("^(%a+)_")
          local mex = UnitDefNames[side .. "_t1_eco_metalextractor"]
          local near = {}
          for i = 1, #spots do
            local s = spots[i]
            near[#near + 1] = { d = math.sqrt((s.x - x) ^ 2 + (s.z - z) ^ 2), s = s }
          end
          table.sort(near, function(a, b) return a.d < b.d end)
          local parts = {}
          for i = 1, math.min(4, #near) do
            local s = near[i].s
            parts[#parts + 1] = ("d=%d test=%s units=%d"):format(near[i].d,
              mex and tostring(Spring.TestBuildOrder(mex.id, s.x, s.y, s.z, 0)) or "?", #Spring.GetUnitsInCylinder(s.x, s.z, 128))
          end
          Spring.Echo(("[AIPROBE] team %d commander at %d,%d nearest spots: %s"):format(teamID, x, z, table.concat(parts, " | ")))
        end
      end
    end
  end
  if n % 1800 == 0 or n >= LIMIT then
    for _, teamID in ipairs(Spring.GetTeamList()) do
      if teamID ~= gaia then
        local counts = {}
        for _, uid in ipairs(Spring.GetTeamUnits(teamID)) do
          local ud = UnitDefs[Spring.GetUnitDefID(uid)]
          if ud then
            local c = Class(ud)
            counts[c] = (counts[c] or 0) + 1
          end
        end
        local parts = {}
        for _, c in ipairs({ "com", "con", "fac", "mex", "bld", "def", "army", "air" }) do
          parts[#parts + 1] = c .. "=" .. (counts[c] or 0)
        end
        local mc, ms, _, mi = Spring.GetTeamResources(teamID, "metal")
        local ec, es, _, ei = Spring.GetTeamResources(teamID, "energy")
        Spring.Echo(("[AIPROBE] f=%d team %d (%s) %s M %d/%d +%.1f E %d/%d +%.0f kills=%d losses=%d comdead=%d"):format(
          n, teamID, Spring.GetTeamLuaAI(teamID) or "human", table.concat(parts, " "),
          mc or 0, ms or 0, mi or 0, ec or 0, es or 0, ei or 0, kills[teamID] or 0, losses[teamID] or 0, comDeaths[teamID] or 0))
        -- production: what the team has finished so far, and what its factories are doing right now
        local b = built[teamID] or {}
        local bp = {}
        for _, c in ipairs({ "con", "mex", "bld", "def", "army", "air" }) do bp[#bp + 1] = c .. "=" .. (b[c] or 0) end
        local fp = {}
        for _, uid in ipairs(Spring.GetTeamUnits(teamID)) do
          local ud = UnitDefs[Spring.GetUnitDefID(uid)]
          if ud and ud.isFactory then
            local q = Spring.GetFullBuildQueue(uid, 0) or {}
            local head = Spring.GetFactoryCommands(uid, 1)
            local busy = Spring.GetUnitIsBuilding(uid)
            local _, _, _, _, bp2 = Spring.GetUnitHealth(uid)
            local first = q[1] and next(q[1])
            fp[#fp + 1] = ("%s[q=%d %s%s%s]"):format(ud.name:gsub("^%a+_t%d_lab_", ""), #q,
              busy and "building" or "idle", (head and head[1] and head[1].id == CMD.WAIT) and " WAIT" or "",
              (bp2 or 1) < 1 and " unfinished" or "")
          end
        end
        Spring.Echo(("[AIPROBE]   built %s | factories: %s"):format(table.concat(bp, " "), table.concat(fp, " ")))
      end
    end
  end
  if n >= LIMIT then
    Spring.Echo("[AIPROBE] done")
    Spring.SendCommands("quitforce")
  end
end

-- modoption aidebugfrom=<frame>: from that frame on, every unit creation and death is echoed (crash hunting)
local DEBUG_FROM = tonumber(opt.aidebugfrom)
function gadget:UnitCreated(unitID, unitDefID, unitTeam, builderID)
  if DEBUG_FROM and Spring.GetGameFrame() >= DEBUG_FROM then
    local x, y, z = Spring.GetUnitPosition(unitID)
    Spring.Echo(("[AIPROBE] f=%d created %s team %d at %d,%d,%d by %s"):format(Spring.GetGameFrame(), UnitDefs[unitDefID].name, unitTeam,
      x or 0, y or 0, z or 0, builderID and (UnitDefs[Spring.GetUnitDefID(builderID) or 0] or {}).name or "?"))
  end
end

function gadget:UnitFinished(unitID, unitDefID, unitTeam)
  local ud = UnitDefs[unitDefID]
  if not ud then return end
  local b = built[unitTeam]
  if not b then b = {}; built[unitTeam] = b end
  local c = Class(ud)
  b[c] = (b[c] or 0) + 1
end

function gadget:UnitDestroyed(unitID, unitDefID, unitTeam, attackerID, attackerDefID, attackerTeam)
  if DEBUG_FROM and Spring.GetGameFrame() >= DEBUG_FROM then
    Spring.Echo(("[AIPROBE] f=%d destroyed %s team %d"):format(Spring.GetGameFrame(), UnitDefs[unitDefID].name, unitTeam))
  end
  losses[unitTeam] = (losses[unitTeam] or 0) + 1
  local ud = UnitDefs[unitDefID]
  if ud and ud.customParams and ud.customParams.iscommander then
    comDeaths[unitTeam] = (comDeaths[unitTeam] or 0) + 1
    Spring.Echo(("[AIPROBE] f=%d team %d lost its commander"):format(Spring.GetGameFrame(), unitTeam))
  end
  if attackerTeam and attackerTeam ~= unitTeam and not Spring.AreTeamsAllied(attackerTeam, unitTeam) then
    kills[attackerTeam] = (kills[attackerTeam] or 0) + 1
  end
end

end
