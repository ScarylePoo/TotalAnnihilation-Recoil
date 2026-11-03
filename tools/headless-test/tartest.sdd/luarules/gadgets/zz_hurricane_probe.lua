function gadget:GetInfo()
  return { name = "Hurricane Probe", layer = 1004, enabled = true }
end
-- Runs with AIM=1 run.sh, beside the walker aim probe. Logs [HARNESS] hurri ...: the Hurricane's belly gun, tail and wing fold in the air and on the
-- ground. Two immune Hurricanes (one attacking a parked tank, one attacking a flying enemy scout), then a move with land-when-idle, report:
-- landed gun/tail positions, shots and hits per weapon and target kind, barrel pitch and angle off the target while the laser fires, lowest clearance of
-- the barrels on the way down. Piece y is unit-frame: y = 0 is the wheels-down plane, the belly is at 0.2.
if not gadgetHandler:IsSyncedCode() or not (Spring.GetModOptions() or {}).aimonly then return end

local function log(...) Spring.Echo("[HARNESS] hurri", ...) end

local T0 = 40
local LAND_AT = T0 + 750
local END_AT = T0 + 1470   -- the walker probe quits at frame 1535
local X, Z = 300, 300

local protected, planes = {}, {}
local byUid = {}
local LASER = WeaponDefNames["core_hurricane_laser"].id
local BOMB = WeaponDefNames["core_hurricane_bomb"].id

function gadget:Initialize() Script.SetWatchWeapon(BOMB, true) end
function gadget:ProjectileCreated(_, owner, weaponDefID)
  local p = owner and byUid[owner]
  if p and weaponDefID == BOMB then
    p.bombProj = (p.bombProj or 0) + 1
    if p.bombProj == 1 then log(p.name, "first bomb at frame", Spring.GetGameFrame()) end
  end
end

function gadget:UnitPreDamaged(uid, udid, _, damage, _, weaponDefID, _, attacker)
  local p = attacker and byUid[attacker]
  if p and weaponDefID and damage > 0 then
    local kind = UnitDefs[udid].canFly and "air" or "ground"
    if weaponDefID == LASER then p.hit["laser_" .. kind] = (p.hit["laser_" .. kind] or 0) + 1 end
    if weaponDefID == BOMB then p.hit["bomb_" .. kind] = (p.hit["bomb_" .. kind] or 0) + 1 end
  end
  if protected[uid] then return 0, 0 end
end

local function rot(uid, piece, axis)
  local a = {Spring.UnitScript.CallAsUnit(uid, Spring.UnitScript.GetPieceRotation, piece)}
  return math.deg(a[axis] or 0)
end

local function pieces(p)
  local m, uid = p.map, p.uid
  local _, ty = Spring.GetUnitPiecePosition(uid, m.turret)
  local _, by = Spring.GetUnitPiecePosition(uid, m.barrels)
  local _, ly = Spring.GetUnitPiecePosition(uid, m.flare1)
  local _, tl = Spring.GetUnitPiecePosition(uid, m.tail2)
  return string.format("turret y %.2f, barrels y %.2f, flare1 y %.2f, tail2 hinge y %.2f rot z %.1f, wing2 rot z %.1f, barrels rot x %.1f",
    ty, by, ly, tl, rot(uid, m.tail2, 3), rot(uid, m.wing2, 3), rot(uid, m.barrels, 1))
end

local function agl(uid)
  local x, y, z = Spring.GetUnitBasePosition(uid)
  return y - math.max(Spring.GetGroundHeight(x, z), 0)
end

-- barrel axis from the flare's emit direction (+z along the barrels), world space
local function aimCheck(p, tx, ty, tz)
  local fx, fy, fz, dx, dy, dz = Spring.GetUnitPiecePosDir(p.uid, p.map.flare1)
  local vx, vy, vz = tx - fx, ty - fy, tz - fz
  local vl, dl = math.sqrt(vx*vx + vy*vy + vz*vz), math.sqrt(dx*dx + dy*dy + dz*dz)
  if vl < 1 or dl < 1e-3 then return end
  local off = math.deg(math.acos(math.max(-1, math.min(1, (dx*vx + dy*vy + dz*vz) / (vl * dl)))))
  return off, math.deg(math.asin(dy / dl)), math.deg(math.asin(vy / vl))
end

local function spawnPlane(name, x, z, team)
  local uid = Spring.CreateUnit("core_t2_air_hurricane", x, Spring.GetGroundHeight(x, z), z, 0, team)
  protected[uid] = true
  local p = {uid = uid, name = name, map = Spring.GetUnitPieceMap(uid), hit = {}, bombs = 0, shots = 0, fired = {}, landedShots = 0,
             clear = 1e9, flightY = nil}
  byUid[uid] = p
  planes[#planes + 1] = p
  return p
end

local tank, gunship
function gadget:GameFrame(f)
  if f == T0 then
    local ud = UnitDefNames["core_t2_air_hurricane"]
    log("def weapons", #ud.weapons, "laser maxAngleDif cos", ud.weapons[2].maxAngleDif, "dir", ud.weapons[2].mainDirX, ud.weapons[2].mainDirY, ud.weapons[2].mainDirZ,
      "onlyTargets", (function() local s = "" for k in pairs(ud.weapons[2].onlyTargets or {}) do s = s .. k .. " " end return s end)())
    tank = Spring.CreateUnit("arm_t1_veh_flash", X + 650, Spring.GetGroundHeight(X + 650, Z), Z, 0, 1)
    protected[tank] = true
    spawnPlane("attacker", X, Z, 0)
    local q = spawnPlane("escort", X, Z + 2200, 0)
    gunship = Spring.CreateUnit("arm_t1_air_peeper", X + 300, Spring.GetGroundHeight(X + 300, Z + 2200), Z + 2200, 0, 1)
    protected[gunship] = true
    q.isEscort = true
    for i = 0, 8 do    -- back and forth over the escort's position
      Spring.GiveOrderToUnit(gunship, CMD.MOVE, {X + 100 + (i % 2) * 400, 0, Z + 2200}, {"shift"})
    end
  end
  if f < T0 + 1 then return end
  local t = f - T0
  for _, p in ipairs(planes) do
    if Spring.ValidUnitID(p.uid) then
      if t == 2 then log(p.name, "just spawned, agl", string.format("%.1f:", agl(p.uid)), pieces(p)) end
      if t == 30 then
        log(p.name, "landed, agl", string.format("%.1f:", agl(p.uid)), pieces(p))
        if p.isEscort then
          Spring.GiveOrderToUnit(p.uid, CMD.IDLEMODE, {0}, {})
          Spring.GiveOrderToUnit(p.uid, CMD.MOVE, {X + 300, 0, Z + 1500}, {})
          Spring.GiveOrderToUnit(p.uid, CMD.ATTACK, {gunship}, {"shift"})
        else
          Spring.GiveOrderToUnit(p.uid, CMD.ATTACK, {tank}, {})
        end
      end
      local h = agl(p.uid)
      local rb = Spring.GetUnitWeaponState(p.uid, 1, "reloadFrame")
      if rb and rb ~= p.r1 then
        if p.r1 then p.bombs = p.bombs + 1 end
        p.r1 = rb
      end
      local r1 = Spring.GetUnitWeaponState(p.uid, 2, "reloadFrame")
      if r1 and r1 ~= p.r2 then
        if p.r2 then
          p.shots = p.shots + 1
          if h < 10 then p.landedShots = p.landedShots + 1 end
          local kind, _, tgt = Spring.GetUnitWeaponTarget(p.uid, 2)
          local tx, ty, tz
          if kind == 1 then tx, ty, tz = Spring.GetUnitPosition(tgt) end
          local off, bp, tp
          if tx then off, bp, tp = aimCheck(p, tx, ty, tz) end
          if off then
            local air = UnitDefs[Spring.GetUnitDefID(tgt)].canFly
            local tag = air and "air" or "ground"
            local a = p[tag] or {n = 0, off = 0, maxoff = 0, lo = 90, tlo = 90}
            p[tag] = a
            a.n, a.off, a.maxoff = a.n + 1, a.off + off, math.max(a.maxoff, off)
            a.lo, a.tlo = math.min(a.lo, bp), math.min(a.tlo, tp)
            if a.n == 1 or a.n % 10 == 0 then
              log(p.name, string.format("laser shot at %s #%d: off target %.1f deg, barrel pitch %.1f, target pitch %.1f, agl %.0f; flare1 y %.2f", tag, a.n, off, bp, tp, h, select(2, Spring.GetUnitPiecePosition(p.uid, p.map.flare1))))
            end
          end
        end
        p.r2 = r1
      end
      if not p.flightY and h > 200 and t > 200 then
        p.flightY = true
        log(p.name, "flying, agl", string.format("%.1f:", h), pieces(p))
      end
      if t == LAND_AT - T0 then
        log(p.name, "before land: agl", string.format("%.1f;", h), pieces(p))
        log(p.name, "weapons so far: bombs dropped", p.bombs, "laser shots", p.shots, "hits", (function() local s = "" for k, v in pairs(p.hit) do s = s .. k .. "=" .. v .. " " end return s end)())
        p.shotsBeforeLand = p.shots
        Spring.GiveOrderToUnit(p.uid, CMD.FIRE_STATE, {0}, {})
        Spring.GiveOrderToUnit(p.uid, CMD.IDLEMODE, {1}, {})
        Spring.GiveOrderToUnit(p.uid, CMD.MOVE, {X + 100, 0, Z + 200 + (p.isEscort and 2000 or 0)}, {})
        p.landing = true
      end
      if p.landing then
        local _, ly = Spring.GetUnitPiecePosition(p.uid, p.map.flare1)
        local _, by = Spring.GetUnitPiecePosition(p.uid, p.map.barrels)
        local lowest = h + math.min(ly, by - 1.45)
        if lowest < p.clear then p.clear, p.clearH = lowest, h end
        if h < 120 and not p.touched and t % 5 == 0 then log(p.name, string.format("descent t %d agl %.1f: turret y %.2f flare1 y %.2f wing2 rot %.0f", t, h, select(2, Spring.GetUnitPiecePosition(p.uid, p.map.turret)), ly, rot(p.uid, p.map.wing2, 3))) end
        if h < 0.1 and not p.touched then p.touched = true; log(p.name, string.format("touchdown t %d: turret y %.2f, flare1 y %.2f", t, select(2, Spring.GetUnitPiecePosition(p.uid, p.map.turret)), ly)) end
        local st = Spring.GetUnitMoveTypeData(p.uid)
        if st and st.aircraftState ~= p.ast then
          log(p.name, "air state", tostring(st.aircraftState), string.format("agl %.1f:", h), pieces(p))
          p.ast = st.aircraftState
        end
      end
      if t == END_AT - T0 - 5 then
        log(p.name, "end, agl", string.format("%.1f:", h), pieces(p))
        for _, tag in ipairs({"air", "ground"}) do
          local a = p[tag]
          if a then log(p.name, string.format("laser at %s: %d shots, off target avg %.1f max %.1f deg, lowest barrel pitch %.1f, lowest target pitch %.1f", tag, a.n, a.off / a.n, a.maxoff, a.lo, a.tlo)) end
        end
        log(p.name, string.format("totals: bombs %d, laser shots %d (at agl<10: %d), lowest gun clearance %.1f at agl %.1f; bomb projectiles %d; hits %s",
          p.bombs, p.shots, p.landedShots, p.clear, p.clearH or -1, p.bombProj or 0, (function() local s = "" for k, v in pairs(p.hit) do s = s .. k .. "=" .. v .. " " end return s end)()))
      end
    end
  end
  if t == END_AT - T0 then log("DONE") end
end
