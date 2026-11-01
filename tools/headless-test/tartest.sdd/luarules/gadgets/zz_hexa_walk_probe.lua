function gadget:GetInfo()
  return { name = "Hexa Walk Probe", layer = 1001, enabled = true }
end

-- Checks walk.Hexa (scripts/headers/walk.lua) on every hexapod def (units with an `rmfoot` piece): the leg calibration
-- result (hexaWalkCalib rules param), the rest splay (front feet ahead of the middle feet, rear feet behind), and while
-- the harness's fight order moves them: how high the feet lift above their rest height, how far below it they go
-- (into the ground = a wrong lift sign), and how far each foot travels forward/back. Logs as [HARNESS] hexa ...
if not gadgetHandler:IsSyncedCode() then return end

local SPAWN0 = 10
local LEGS = {"rf", "lf", "rm", "lm", "rb", "lb"}
local probes = {}

local function log(...) Spring.Echo("[HARNESS] hexa", ...) end

local function footPos(p, i)
  local x, y, z = Spring.GetUnitPiecePosition(p.uid, p.feet[i])
  return x, y, z
end

function gadget:GameFrame(frame)
  local f = frame - (SPAWN0 + #UnitDefs)
  if f == 40 then
    local seen = {}
    for _, uid in ipairs(Spring.GetAllUnits()) do
      local udid = Spring.GetUnitDefID(uid)
      local map = Spring.GetUnitPieceMap(uid)
      if not seen[udid] and map and map.rmfoot then
        seen[udid] = true
        local p = {uid = uid, name = UnitDefs[udid].name, feet = {}, rest = {}, lo = {}, hi = {}, zlo = {}, zhi = {}}
        for i, l in ipairs(LEGS) do
          p.feet[i] = map[l .. "foot"]
          local x, y, z = footPos(p, i)
          p.rest[i] = {x, y, z}
          p.lo[i], p.hi[i], p.zlo[i], p.zhi[i] = y, y, z, z
        end
        p.x0, _, p.z0 = Spring.GetUnitPosition(uid)
        probes[#probes + 1] = p
        local r = p.rest
        log(p.name, "calib", tostring(Spring.GetUnitRulesParam(uid, "hexaWalkCalib")),
          string.format("rest z front %.1f/%.1f mid %.1f/%.1f rear %.1f/%.1f, splay %s", r[1][3], r[2][3], r[3][3], r[4][3],
            r[5][3], r[6][3], (r[1][3] > r[3][3] and r[2][3] > r[4][3] and r[5][3] < r[3][3] and r[6][3] < r[4][3]) and "OK" or "WRONG"))
      end
    end
  elseif f > 50 and f <= 650 and f % 3 == 0 then
    for _, p in ipairs(probes) do
      if Spring.ValidUnitID(p.uid) then
        for i = 1, 6 do
          local _, y, z = footPos(p, i)
          if y < p.lo[i] then p.lo[i] = y end
          if y > p.hi[i] then p.hi[i] = y end
          if z < p.zlo[i] then p.zlo[i] = z end
          if z > p.zhi[i] then p.zhi[i] = z end
        end
      end
    end
  elseif f == 651 then
    for _, p in ipairs(probes) do
      local lift, sink, swing = 0, 0, 0
      for i = 1, 6 do
        lift = math.max(lift, p.hi[i] - p.rest[i][2])
        sink = math.max(sink, p.rest[i][2] - p.lo[i])
        swing = swing + (p.zhi[i] - p.zlo[i]) / 6
      end
      local moved = -1
      if Spring.ValidUnitID(p.uid) then
        local x, _, z = Spring.GetUnitPosition(p.uid)
        moved = math.sqrt((x - p.x0) ^ 2 + (z - p.z0) ^ 2)
      end
      log(p.name, string.format("walked %.0f elmos: feet lift max %.2f, sink max %.2f, mean fore-aft travel %.2f -> %s",
        moved, lift, sink, swing, (lift > 0.3 and sink < 0.25 and swing > 0.5) and "ANIMATES" or "CHECK"))
    end
  end
end
