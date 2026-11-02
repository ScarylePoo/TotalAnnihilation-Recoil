function gadget:GetInfo()
  return { name = "Hexa Walk Probe", layer = 1001, enabled = true }
end

-- Checks walk.Hexa (scripts/headers/walk.lua) on every hexapod def (units with an `rmfoot` piece): the leg calibration
-- result (hexaWalkCalib rules param), the rest splay (front feet ahead of the middle feet, rear feet behind), and while
-- they move and fight (sampled every frame for 600 frames, or until the unit dies): how high the feet lift above their rest height, how far below it they go
-- (into the ground = a wrong lift sign), and how far each foot travels forward/back. Logs as [HARNESS] hexa ...
-- The probed unit is made immune (UnitPreDamaged returns 0 damage) and given its own move order at once, so the sample window covers
-- real walking: the first run sampled the Spider and Scarab before the harness's orders (they idled, then died).
-- The report also gives the distance the body moved, so 'feet still while the unit moves' can be told from 'unit idle'.
if not gadgetHandler:IsSyncedCode() then return end

local LEGS = {"rf", "lf", "rm", "lm", "rb", "lb"}
local probes = {}
local seenDef = {}

local function log(...) Spring.Echo("[HARNESS] hexa", ...) end

local function footPos(p, i)
  local x, y, z = Spring.GetUnitPiecePosition(p.uid, p.feet[i])
  return x, y, z
end

-- register the first unit of each hexapod def as soon as it exists (the harness spawns enemies side by side and they
-- start shooting at once: a fixed sampling frame missed units that had already died)
local pending = {}
local protected = {}     -- probed units take no damage (Recoil has no SetUnitNoDamage; UnitPreDamaged zeroes it)
function gadget:UnitPreDamaged(uid)
  if protected[uid] then return 0, 0 end
end

function gadget:UnitCreated(uid, udid)
  if seenDef[udid] then return end
  local map = Spring.GetUnitPieceMap(uid)
  if map and map.rmfoot then
    seenDef[udid] = true
    protected[uid] = true
    pending[#pending + 1] = {uid = uid, udid = udid, map = map}
  end
end

local function report(p)
  if p.done then return end
  p.done = true
  local lift, sink, swing = 0, 0, 0
  for i = 1, 6 do
    lift = math.max(lift, p.hi[i] - p.rest[i][2])
    sink = math.max(sink, p.rest[i][2] - p.lo[i])
    swing = swing + (p.zhi[i] - p.zlo[i]) / 6
  end
  local moved = 0
  if p.start and Spring.ValidUnitID(p.uid) then
    local x, _, z = Spring.GetUnitPosition(p.uid)
    moved = math.sqrt((x - p.start[1]) ^ 2 + (z - p.start[2]) ^ 2)
  end
  log(p.name, string.format("over %d frames: body moved %.0f, path %.0f, max speed %.2f; feet lift max %.2f, sink max %.2f, mean fore-aft travel %.2f -> %s",
    p.frames, moved, p.path, p.vmax, lift, sink, swing, (lift > 0.3 and sink < 0.25 and swing > 0.5) and "ANIMATES" or "CHECK"))
end

function gadget:UnitDestroyed(uid)
  for _, p in ipairs(probes) do
    if p.uid == uid then report(p) end
  end
end

function gadget:GameFrame(frame)
  for _, q in ipairs(pending) do      -- rest pose one frame after creation (Create has calibrated and splayed)
    if Spring.ValidUnitID(q.uid) then
      local p = {uid = q.uid, name = UnitDefs[q.udid].name, feet = {}, rest = {}, lo = {}, hi = {}, zlo = {}, zhi = {}, frames = 0,
                 path = 0, vmax = 0}
      for i, l in ipairs(LEGS) do
        p.feet[i] = q.map[l .. "foot"]
        local x, y, z = footPos(p, i)
        p.rest[i] = {x, y, z}
        p.lo[i], p.hi[i], p.zlo[i], p.zhi[i] = y, y, z, z
      end
      probes[#probes + 1] = p
      -- walk it: a move order of its own toward the map centre (the harness's later fight order goes the same way)
      local ux, uy, uz = Spring.GetUnitPosition(q.uid)
      p.start = {ux, uz}; p.last = {ux, uz}
      Spring.GiveOrderToUnit(q.uid, CMD.MOVE, {Game.mapSizeX / 2, 0, Game.mapSizeZ / 2}, {})
      local r = p.rest
      log(p.name, "calib", tostring(Spring.GetUnitRulesParam(q.uid, "hexaWalkCalib")),
        string.format("rest z front %.1f/%.1f mid %.1f/%.1f rear %.1f/%.1f, splay %s", r[1][3], r[2][3], r[3][3], r[4][3],
          r[5][3], r[6][3], (r[1][3] > r[3][3] and r[2][3] > r[4][3] and r[5][3] < r[3][3] and r[6][3] < r[4][3]) and "OK" or "WRONG"))
    end
  end
  pending = {}
  for _, p in ipairs(probes) do
    if not p.done and Spring.ValidUnitID(p.uid) then
      p.frames = p.frames + 1
      local ux, _, uz = Spring.GetUnitPosition(p.uid)
      p.path = p.path + math.sqrt((ux - p.last[1]) ^ 2 + (uz - p.last[2]) ^ 2); p.last = {ux, uz}
      local vx, _, vz = Spring.GetUnitVelocity(p.uid)
      p.vmax = math.max(p.vmax, math.sqrt(vx * vx + vz * vz))
      for i = 1, 6 do
        local _, y, z = footPos(p, i)
        if y < p.lo[i] then p.lo[i] = y end
        if y > p.hi[i] then p.hi[i] = y end
        if z < p.zlo[i] then p.zlo[i] = z end
        if z > p.zhi[i] then p.zhi[i] = z end
      end
      if p.frames >= 600 then report(p) end
    end
  end
end
