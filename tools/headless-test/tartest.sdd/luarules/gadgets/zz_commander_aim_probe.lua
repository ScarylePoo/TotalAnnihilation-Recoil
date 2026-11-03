function gadget:GetInfo()
  return { name = "Commander Aim Probe", layer = 1002, enabled = true }
end
local _opt = Spring.GetModOptions() or {}
if _opt.aimonly or _opt.gaponly then return end   -- run.sh AIM=1 / GAP=1 run only their own probe

-- Do the commanders' arms point at what they shoot at and build? An immune commander and decoy of each side get, in turn, a laser
-- ground attack far and near, a D-gun, a build order, then a stop. At the end of each phase logs the angle between the arm (pivot ->
-- a piece along the barrel) and the line from the muzzle to the target; "rest" logs the arm's pitch from straight along its
-- hanging/forward axis instead. Logs as [HARNESS] aim ... (about 0 = on target; the arm's offset from the torso adds a few degrees).
if not gadgetHandler:IsSyncedCode() then return end

local ARM = {laser = {"nanolath", "nanospray", "lfirept"}, nano = {"nanolath", "nanospray", "nanospray"}, dgun = {"biggun", "rbigflash", "rbigflash"}}
local CORE = {laser = {"l_nano", "nanospray", "mlasflsh"}, nano = {"l_nano", "nanospray", "mlasflsh"}, dgun = {"r_dgun", "bigflsh", "bigflsh"}}
local SUBJECTS = {
  {"arm_commander", ARM}, {"arm_t2_bot_decoycommander", ARM},
  {"core_commander", CORE}, {"core_t2_bot_decoycommander", CORE},
}
local units = {}
local protected = {}
function gadget:UnitPreDamaged(uid)
  if protected[uid] then return 0, 0 end
end

local function log(...) Spring.Echo("[HARNESS] aim", ...) end

-- piece ORIGIN in world space: GetUnitPiecePosDir gives the emit vertex instead, which is off the barrel on flare pieces.
-- GetUnitPiecePosition's x runs along the unit's right vector (it reads mirrored against the model).
local function pieceWorld(uid, p)
  local x, y, z = Spring.GetUnitPiecePosition(uid, p)
  local bx, by, bz = Spring.GetUnitBasePosition(uid)
  local f, u, r = Spring.GetUnitVectors(uid)      -- three {x, y, z} tables
  return bx + r[1] * x + u[1] * y + f[1] * z, by + r[2] * x + u[2] * y + f[2] * z, bz + r[3] * x + u[3] * y + f[3] * z
end

local function measure(s, name, part, tx, ty, tz)
  local m = s.map
  local px, py, pz = pieceWorld(s.uid, m[part[1]])
  local ax, ay, az = pieceWorld(s.uid, m[part[2]])
  local fx, fy, fz = pieceWorld(s.uid, m[part[3]])
  local dx, dy, dz = ax - px, ay - py, az - pz
  local tvx, tvy, tvz = tx - fx, ty - fy, tz - fz
  local dl, tl = math.sqrt(dx*dx + dy*dy + dz*dz), math.sqrt(tvx*tvx + tvy*tvy + tvz*tvz)
  local c = (dx*tvx + dy*tvy + dz*tvz) / (dl * tl)
  local deg = math.deg(math.acos(math.max(-1, math.min(1, c))))
  local bx, _, bz = Spring.GetUnitBasePosition(s.uid)
  log(s.name, name, string.format("off target %.1f deg; arm pitch %.1f, target pitch %.1f; arm yaw %.1f, target yaw %.1f; unit moved %.0f, body heading %.1f; order %s",
    deg, math.deg(math.asin(dy / dl)), math.deg(math.asin(tvy / tl)), math.deg(math.atan2(dx, dz)), math.deg(math.atan2(tvx, tvz)),
    math.sqrt((bx - s.x)^2 + (bz - s.z)^2), Spring.GetUnitHeading(s.uid) * 360 / 65536, tostring((Spring.GetUnitCommands(s.uid, 1) or {})[1] and Spring.GetUnitCommands(s.uid, 1)[1].id)))
end

local function order(s, cmd, tx, tz, extra)
  s.t = {tx, tz}
  local p = {tx, Spring.GetGroundHeight(tx, tz), tz}
  if extra then p[4] = extra end
  Spring.GiveOrderToUnit(s.uid, cmd, p, {})
end

local PHASES = {
  {at = 0,   go = function(s) order(s, CMD.ATTACK, s.x + 90, s.z + 180) end},
  {at = 150, sample = {"laser far", "laser"}},
  {at = 151, go = function(s) order(s, CMD.ATTACK, s.x - 40, s.z + 60) end},
  {at = 300, sample = {"laser near", "laser"}},
  {at = 301, go = function(s) Spring.GiveOrderToUnit(s.uid, CMD.STOP, {}, {}) ; order(s, CMD.MANUALFIRE, s.x + 100, s.z + 120) end},
  {at = 345, sample = {"dgun", "dgun"}},
  {at = 421, go = function(s) Spring.GiveOrderToUnit(s.uid, CMD.STOP, {}, {}) end},
  {at = 760, go = function(s)
      local b = UnitDefs[s.udid].buildOptions[1]
      if b then order(s, -b, s.x - 80, s.z + 70, 0) end
    end},
  {at = 900, sample = {"build", "nano"}},
  {at = 901, go = function(s) Spring.GiveOrderToUnit(s.uid, CMD.STOP, {}, {}) end},
  {at = 1200, sample = {"rest", "nano"}},
}

local t0
function gadget:GameFrame(frame)
  if not t0 then
    if frame < 60 + #UnitDefs + 60 then return end       -- after harness SPAWN0 + all defs + orders; see zz_test_harness.lua
    t0 = frame
    for i, sub in ipairs(SUBJECTS) do
      local ud = UnitDefNames[sub[1]]
      if ud then
        local x, z = 300 + (i - 1) * 500, Game.mapSizeZ - 500
        local uid = Spring.CreateUnit(ud.id, x, Spring.GetGroundHeight(x, z), z, 0, 1)
        if uid then
          protected[uid] = true
          Spring.GiveOrderToUnit(uid, CMD.FIRE_STATE, {0}, {})
          units[#units + 1] = {uid = uid, udid = ud.id, name = sub[1], parts = sub[2], x = x, z = z, map = Spring.GetUnitPieceMap(uid)}
        end
      end
    end
  end
  local f = frame - t0 - 30
  for _, ph in ipairs(PHASES) do
    if ph.at == f then
      for _, s in ipairs(units) do
        if Spring.ValidUnitID(s.uid) then
          if ph.go then ph.go(s)
          elseif s.t and not (ph.sample[1] == "build" and not UnitDefs[s.udid].buildOptions[1]) then
            measure(s, ph.sample[1], s.parts[ph.sample[2]], s.t[1], Spring.GetGroundHeight(s.t[1], s.t[2]), s.t[2])
          end
        end
      end
    end
  end
end
