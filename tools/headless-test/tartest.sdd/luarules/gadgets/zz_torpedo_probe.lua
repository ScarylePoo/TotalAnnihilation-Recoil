function gadget:GetInfo()
  return { name = "Torpedo Probe", layer = 1006, enabled = true }
end

-- TORP=<depth> run.sh: every unit with a TorpedoLauncher weapon against targets in water <depth> elmos deep.
-- TORPKIND picks the targets, comma separated (default ship,sub,moving,shore):
--   ship    a surface ship, still          sub     a submarine, still          moving  a surface ship on a circuit
--   shore   a ship just off a beach, with a land unit on the beach behind it (hits on that one are "bystander")
--   land    a land unit on an island       air     a plane circling over water (both: fire state "fire at will" as well)
-- Damage is cancelled, so targets live and shots stay comparable. One [PROBE] line per attacker, weapon and target:
-- shots, hits on the target, hits on the bystander, explosions on the seabed, deepest point and water-entry speed.
local mo = Spring.GetModOptions() or {}
if not gadgetHandler:IsSyncedCode() or not mo.torpprobe then return end

local DEPTH = -tonumber(mo.torpprobe)
local KINDS = {}
for k in tostring(mo.torpkind or "ship,sub,moving,shore"):gmatch("[^,]+") do KINDS[#KINDS + 1] = k end
local CELL, TEAM, FRAME0, FRAMES = 1700, 1, 60, 1800
local SHIP, SUB, LANDUNIT, PLANE = "arm_t1_sea_skeeter", "arm_t1_sea_lurker", "arm_t1_bot_peewee", "arm_t1_air_peeper"

local function isTorp(wdid) local w = WeaponDefs[wdid] return w and w.type == "TorpedoLauncher" end

local cases, byAttacker, shots = {}, {}, {}
do
  local names = {}
  for _, ud in pairs(UnitDefs) do
    local best
    for _, w in ipairs(ud.weapons) do
      if isTorp(w.weaponDef) then best = math.max(best or 0, WeaponDefs[w.weaponDef].range) end
    end
    if best then names[#names + 1] = {ud.name, best, ud.canFly} end
  end
  table.sort(names, function(a, b) return a[1] < b[1] end)
  local i = 0
  for _, n in ipairs(names) do
    for _, kind in ipairs(KINDS) do
      local c = {a = n[1], range = n[2], air = n[3], kind = kind}
      c.x = 1300 + (i % 9) * CELL
      c.z = 1000 + math.floor(i / 9) * CELL
      c.d = c.air and 800 or n[2] * 0.7
      c.tz = c.z + c.d
      c.w = {}
      cases[#cases + 1] = c
      i = i + 1
    end
  end
end

function gadget:Initialize()
  Spring.SetHeightMapFunc(function()
    for x = 0, Game.mapSizeX, 8 do
      for z = 0, Game.mapSizeZ, 8 do Spring.SetHeightMap(x, z, x < 300 and 20 or DEPTH) end
    end
    for _, c in ipairs(cases) do
      local x0, x1, z0, z1
      if c.kind == "shore" then x0, x1, z0, z1 = c.x - 300, c.x + 300, c.tz + 72, c.tz + 500 end
      if c.kind == "land" then x0, x1, z0, z1 = c.x - 240, c.x + 240, c.tz - 240, c.tz + 240 end
      if x0 then
        for x = x0 - x0 % 8, x1, 8 do
          for z = z0 - z0 % 8, z1, 8 do Spring.SetHeightMap(x, z, 20) end
        end
      end
    end
  end)
end

local function log(...) Spring.Echo("[PROBE]", ...) end

local function rec(c, wdid)
  c.w[wdid] = c.w[wdid] or {shots = 0, hits = 0, bystander = 0, seabed = 0, other = 0, dive = 0, entry = 0, entries = 0}
  return c.w[wdid]
end

function gadget:UnitPreDamaged(uid, _, _, damage, _, weaponDefID, _, attacker)
  local c = attacker and byAttacker[attacker]
  if c and weaponDefID and isTorp(weaponDefID) then
    local r = rec(c, weaponDefID)
    if uid == c.target then r.hits = r.hits + 1
    elseif uid == c.bystander then r.bystander = r.bystander + 1
    else r.other = r.other + 1 r.otherName = UnitDefs[Spring.GetUnitDefID(uid)].name end
  end
  return 0, 0
end

function gadget:ProjectileCreated(pid, owner, weaponDefID)
  local c = owner and byAttacker[owner]
  if c and isTorp(weaponDefID) then
    local r = rec(c, weaponDefID)
    r.shots = r.shots + 1
    shots[pid] = {r = r}
  end
end

function gadget:Explosion(weaponDefID, x, y, z, owner)
  local c = owner and byAttacker[owner]
  if c and isTorp(weaponDefID) and y <= Spring.GetGroundHeight(x, z) + 3 then
    local r = rec(c, weaponDefID)
    r.seabed = r.seabed + 1
  end
  return false
end

local function spawn(name, x, z, team)
  local u = Spring.CreateUnit(name, x, Spring.GetGroundHeight(x, z), z, 0, team)
  if not u then log("SPAWN FAIL", name, x, z) end
  return u
end

local function order(c)
  if not (c.uid and c.target) then return end
  Spring.GiveOrderToUnit(c.uid, CMD.ATTACK, {c.target}, {})
end

local function setup()
  for wd = 0, #WeaponDefs do
    if isTorp(wd) then
      Script.SetWatchProjectile(wd, true)
      if Script.SetWatchExplosion then Script.SetWatchExplosion(wd, true) else Script.SetWatchWeapon(wd, true) end
    end
  end
  Spring.CreateUnit(LANDUNIT, 100, 0, 100, 0, 0)     -- keep both teams alive whatever happens
  Spring.CreateUnit(LANDUNIT, 100, 0, 300, 0, TEAM)
  for _, c in ipairs(cases) do
    local tname = (c.kind == "sub" and SUB) or (c.kind == "land" and LANDUNIT) or (c.kind == "air" and PLANE) or SHIP
    c.uid = spawn(c.a, c.x, c.z, TEAM)
    c.target = spawn(tname, c.x, c.tz, 0)
    if c.kind == "shore" then c.bystander = spawn(LANDUNIT, c.x, c.tz + 110, 0) end
    for _, u in ipairs({c.target, c.bystander}) do
      Spring.GiveOrderToUnit(u, CMD.FIRE_STATE, {0}, {})
      Spring.SetUnitAlwaysVisible(u, true)
    end
    if c.kind == "moving" or c.kind == "air" then
      Spring.GiveOrderToUnit(c.target, CMD.MOVE, {c.x + 250, 0, c.tz}, {})
      Spring.GiveOrderToUnit(c.target, CMD.MOVE, {c.x - 250, 0, c.tz}, {"shift"})
      Spring.GiveOrderToUnit(c.target, CMD.REPEAT, {1}, {})
    end
    if c.uid then
      byAttacker[c.uid] = c
      Spring.SetUnitSensorRadius(c.uid, "sonar", 2000)
      Spring.GiveOrderToUnit(c.uid, CMD.FIRE_STATE, {(c.kind == "land" or c.kind == "air") and 2 or 0}, {})
      order(c)
    end
  end
end

local function report()
  for _, c in ipairs(cases) do
    local ud = c.uid and Spring.ValidUnitID(c.uid) and UnitDefs[Spring.GetUnitDefID(c.uid)]
    local y = c.target and select(2, Spring.GetUnitPosition(c.target)) or -9999
    local ay = c.uid and select(2, Spring.GetUnitPosition(c.uid)) or -9999
    if ud then
      for _, w in ipairs(ud.weapons) do
        local wdid = w.weaponDef
        if isTorp(wdid) and not c[wdid] then
          c[wdid] = true
          local r = rec(c, wdid)
          log("T", string.format("depth=%d kind=%s %s %s shots=%d hits=%d bystander=%d other=%d seabed=%d dive=%.0f entry=%.1f y=%.0f ty=%.0f",
            -DEPTH, c.kind, c.a, WeaponDefs[wdid].name, r.shots, r.hits, r.bystander, r.other, r.seabed, r.dive,
            r.entries > 0 and r.entry / r.entries or 0, ay, y) .. (r.otherName and " otherVictim=" .. r.otherName or ""))
        end
      end
    else
      log("T", string.format("depth=%d kind=%s %s DEAD", -DEPTH, c.kind, c.a))
    end
  end
end

function gadget:GameFrame(f)
  if f == 1 then Spring.SendCommands("cheat 1", "setmaxspeed 200", "setminspeed 200") end
  if f == 30 then setup() end
  if f < FRAME0 then return end
  for pid, s in pairs(shots) do
    local x, y = Spring.GetProjectilePosition(pid)
    if not x then
      shots[pid] = nil
    else
      if y < 0 and not s.wet then
        s.wet = true
        local vx, vy, vz = Spring.GetProjectileVelocity(pid)
        s.r.entry = s.r.entry + math.sqrt(vx * vx + vy * vy + vz * vz)
        s.r.entries = s.r.entries + 1
      end
      if -y > s.r.dive then s.r.dive = -y end
    end
  end
  if f % 150 == 0 then
    for _, c in ipairs(cases) do
      if c.uid and Spring.ValidUnitID(c.uid) and (Spring.GetUnitCommands(c.uid, 0) or 0) == 0 then order(c) end
    end
  end
  if f == FRAME0 + FRAMES then
    report()
    log("end frame", f)
    Spring.SendCommands("quitforce")
  end
end
