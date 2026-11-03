function gadget:GetInfo()
  return { name = "Krogoth Probe", layer = 1002, enabled = true }
end
if (Spring.GetModOptions() or {}).aimonly then return end   -- run.sh --aim runs only the walker aim probe

-- Krogoth and its Gantry, the two biggest models. Logs as [HARNESS] krog ...
-- Walk: the shared biped keys were made for a pelvis height of 23; does cadence/bob scaling hold at H 28 and speed 30?
-- An immune Krogoth (and two reference walkers) walks for 900 frames; per foot: fore-aft reach, lift, sink below its rest height, and "skate":
-- while the foot is planted (lowest 15 % of its height range) how fast it slides over the ground (0 = no skating;
-- reported as a ratio to the body speed). Also pelvis bob, cycle length, and the gun/silo emit heights (aim moves them).
-- GetUnitPiecePosition reports x mirrored against the model (clamp1 is at model x -7.5 and reads +7.5).
-- Gantry: where the nano emit pieces and the build point end up once the yard opens, to compare with the kit's preview.
if not gadgetHandler:IsSyncedCode() then return end

local function log(...) Spring.Echo("[HARNESS] krog", ...) end

-- the harness spawns each def for team 0, then team 1; team 1's copy is the walker because team 0 is wiped out early in
-- the run (about 320 frames after the last spawn), team 0's Krogoth still lives long enough to prove its guns.
-- The Peewee and Morty are reference walkers (the walk's calibration sizes) for the same numbers.
local REF = {core_t3_bot_krogoth = true, arm_t1_bot_peewee = true, core_t2_bot_morty = true}
local seen = {}
local walkers = {}
local shooter, gantry
local protected = {}

function gadget:UnitPreDamaged(uid)
  if protected[uid] then return 0, 0 end
end

function gadget:UnitCreated(uid, udid)
  local n = UnitDefs[udid].name
  seen[n] = (seen[n] or 0) + 1
  if REF[n] and seen[n] == 2 then
    walkers[#walkers + 1] = {uid = uid, name = n, f = 0, feet = {}, hist = {}}
    protected[uid] = true
  elseif n == "core_t3_bot_krogoth" and seen[n] == 1 then
    shooter = {uid = uid, f = 0, shots = {0, 0, 0}, last = {}}
    protected[uid] = true
  elseif n == "core_t3_lab_krogothgantry" and seen[n] == 2 then
    gantry = {uid = uid, f = 0}
    protected[uid] = true
  end
end

local function pp(uid, map, name)
  local x, y, z = Spring.GetUnitPiecePosition(uid, map[name])
  return string.format("%s(%.1f,%.1f,%.1f)", name, x, y, z)
end

local function walkerFrame(p)
  p.f = p.f + 1
  local uid = p.uid
  if not Spring.ValidUnitID(uid) then return true end
  if p.f == 1 then
    p.map = Spring.GetUnitPieceMap(uid)
    local _, y = Spring.GetUnitPiecePosition(uid, p.map.pelvis)
    log(p.name, "walker pelvis y", y, "unitdef speed", UnitDefs[Spring.GetUnitDefID(uid)].speed)
  end
  if p.f % 60 == 1 then     -- the harness's later fight/fire-state orders would stop it to shoot: keep it walking
    Spring.GiveOrderToUnit(uid, CMD.FIRE_STATE, {0}, {})
    Spring.GiveOrderToUnit(uid, CMD.MOVE, {Game.mapSizeX * 0.45, 0, Game.mapSizeZ - 100}, {})
  end
  local vx, _, vz = Spring.GetUnitVelocity(uid)
  local speed = math.sqrt(vx * vx + vz * vz)
  local _, my = Spring.GetUnitPiecePosition(uid, p.map.pelvis)
  p.ylo, p.yhi = math.min(p.ylo or my, my), math.max(p.yhi or my, my)
  p.vmax = math.max(p.vmax or 0, speed)
  p.path = (p.path or 0) + speed
  for _, name in ipairs({"lfoot", "rfoot"}) do
    local x, y, z = Spring.GetUnitPiecePosition(uid, p.map[name])
    local h = p.hist[name] or {}
    p.hist[name] = h
    h[#h + 1] = {y = y, z = z, speed = speed}
  end
  if p.f >= 900 then return true end
end

local function walkerReport(p)
  log(p.name, "walker frames", p.f, string.format("path %.0f, vmax %.2f (elmo/frame), pelvis y %.2f..%.2f",
    p.path or 0, p.vmax or 0, p.ylo or 0, p.yhi or 0))
  for name, h in pairs(p.hist) do
    local ylo, yhi, zlo, zhi = 1e9, -1e9, 1e9, -1e9
    for i = 30, #h do
      ylo, yhi = math.min(ylo, h[i].y), math.max(yhi, h[i].y)
      zlo, zhi = math.min(zlo, h[i].z), math.max(zhi, h[i].z)
    end
    -- planted = low in its own range; unit-frame rearward foot speed against the body's forward speed
    local plantY = ylo + 0.15 * (yhi - ylo)
    local n, slip, body, steps, inPlant = 0, 0, 0, 0, false
    for i = 31, #h do
      local planted = h[i].y <= plantY
      if planted and h[i].speed > 0.3 then
        n = n + 1
        slip = slip + (h[i - 1].z - h[i].z)      -- rearward motion in the unit frame = ground contact if == body speed
        body = body + h[i].speed
      end
      if planted and not inPlant then steps = steps + 1 end
      inPlant = planted
    end
    log(p.name, name, string.format("ankle y %.2f..%.2f, z %.2f..%.2f (reach %.1f), plants %d over %d frames; planted %d frames: foot back %.3f vs body %.3f per frame, stride/ground ratio %.2f",
      ylo, yhi, zlo, zhi, zhi - zlo, steps, #h, n, n > 0 and slip / n or 0, n > 0 and body / n or 0, (body > 0) and slip / body or 0))
  end
end

-- a second Krogoth stays in the fight: its weapons must fire and the aim poses must move the emit pieces
local function shooterFrame(p)
  p.f = p.f + 1
  local uid = p.uid
  if not Spring.ValidUnitID(uid) or p.f >= 1200 then
    log(string.format("shooter over %d frames: shots cannon %d beam %d rocket %d; right flare z max %.1f (forward when aimed), right silo emit y %.1f..%.1f",
      p.f, p.shots[1], p.shots[2], p.shots[3], p.gz or 0, p.slo or 0, p.shi or 0))
    return true
  end
  p.map = p.map or Spring.GetUnitPieceMap(uid)
  local gy = select(3, Spring.GetUnitPiecePosition(uid, p.map.rgunflare))
  local sy = select(2, Spring.GetUnitPiecePosition(uid, p.map.rmispoint))
  p.gz = math.max(p.gz or gy, gy)
  p.slo, p.shi = math.min(p.slo or sy, sy), math.max(p.shi or sy, sy)
  for i = 1, 3 do
    local r = Spring.GetUnitWeaponState(uid, i, "reloadFrame")
    if r and r ~= p.last[i] then
      if p.last[i] then p.shots[i] = p.shots[i] + 1 end
      p.last[i] = r
    end
  end
end

local function gantryFrame(p)
  p.f = p.f + 1
  local uid = p.uid
  if not Spring.ValidUnitID(uid) then return true end
  if p.f == 1 then
    p.map = Spring.GetUnitPieceMap(uid)
    log("gantry closed", pp(uid, p.map, "nano1"), pp(uid, p.map, "gangplank"), pp(uid, p.map, "clamp1"))
    Spring.GiveOrderToUnit(uid, -UnitDefNames["core_t3_bot_krogoth"].id, {}, {})
  end
  if p.f == 900 then
    log("gantry open", pp(uid, p.map, "nano1"), pp(uid, p.map, "nano2"), pp(uid, p.map, "nano3"), pp(uid, p.map, "nano4"))
    log("gantry open", pp(uid, p.map, "gangplank"), pp(uid, p.map, "clamp1"), pp(uid, p.map, "clamp4"), pp(uid, p.map, "arm1a"), pp(uid, p.map, "cranetop"), "building", tostring(Spring.GetUnitIsBuilding(uid)))
    return true
  end
end

function gadget:GameFrame()
  for _, w in ipairs(walkers) do
    if not w.done and walkerFrame(w) then w.done = true; walkerReport(w) end
  end
  if shooter and not shooter.done and shooterFrame(shooter) then shooter.done = true end
  if gantry and not gantry.done and gantryFrame(gantry) then gantry.done = true end
end
