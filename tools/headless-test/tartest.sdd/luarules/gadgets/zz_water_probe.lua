function gadget:GetInfo()
  return { name = "Water Probe", layer = 1005, enabled = true }
end

-- WATER=1 run.sh: hover and ship transports loading and unloading across a shore. The map is a flat plain sloping down to a lake
-- (the shoreline at x = 6200, ship depth from about x = 6300), and each case is a row of its own on the map.
-- Logs [PROBE] lines: order queue, distance, cargo count; attachment while the transport moves; where the cargo ends up.
if not gadgetHandler:IsSyncedCode() or not (Spring.GetModOptions() or {}).waterprobe then return end

local SIZE, SIZEZ = Game.mapSizeX, Game.mapSizeZ
local RAMP0, RAMP1, HIGH, LOW = 6000, 6600, 20, -40
local DEEP = (Spring.GetModOptions() or {}).waterdepth and -tonumber(Spring.GetModOptions().waterdepth) or -150
local TEAM = 1          -- the harness notes team 0 dies some 320 frames after spawn

local function log(...) Spring.Echo("[PROBE]", ...) end
local function fmt(v) return string.format("%.1f", v or -9999) end

function gadget:Initialize()
  Spring.SetHeightMapFunc(function()
    for x = 0, SIZE, 8 do
      local h = x <= RAMP0 and HIGH or x >= RAMP1 and LOW or HIGH + (LOW - HIGH) * (x - RAMP0) / (RAMP1 - RAMP0)
      if x > 7000 then h = DEEP end   -- torpedo and anti-air tests: open water far from the shore cases
      for z = 0, SIZEZ, 8 do Spring.SetHeightMap(x, z, h) end
    end
  end)
end

-- seaplane torpedoes and ship anti-air: per case, shots seen as projectiles and hits per weapon def
local W_CASES = {
  {a = "core_t1_seapl_typhoon", b = "arm_t1_sea_skeeter", order = "attack"},
  {a = "core_t1_seapl_typhoon", b = "arm_t1_sea_lurker",  order = "attack", sonar = true},
  {a = "core_t1_seapl_typhoon", b = "arm_t1_sea_skeeter", order = "auto"},
  {a = "core_t1_seapl_typhoon", b = "arm_t1_sea_lurker",  order = "auto", sonar = true},
  {a = "arm_t2_sea_archer",     b = "arm_t1_air_peeper",  order = "auto", circle = true},
  {a = "arm_t2_sea_archer",     b = "arm_t1_air_peeper",  order = "attack", circle = true},
  {a = "arm_t2_sea_archer",     b = "core_t1_air_fink",   order = "auto", circle = true},
  {a = "arm_t2_sea_archer",     b = "arm_t1_sea_skeeter", order = "auto"},
  {a = "core_t1_seapl_typhoon", b = "arm_t1_sea_skeeter", order = "attack", x = 6800, z = 8000, visible = true},   -- 40 elmos of water
}
local byAttacker = {}
local W_FRAME0, W_FRAMES = 60, 1500

local function pieceWorld(uid, p)
  local x, y, z = Spring.GetUnitPiecePosition(uid, p)
  local bx, by, bz = Spring.GetUnitBasePosition(uid)
  local f, u, r = Spring.GetUnitVectors(uid)
  return bx + r[1] * x + u[1] * y + f[1] * z, by + r[2] * x + u[2] * y + f[2] * z, bz + r[3] * x + u[3] * y + f[3] * z
end

local function weaponRec(c, wdid)
  c.w[wdid] = c.w[wdid] or {shots = 0, hits = 0, damage = 0, name = WeaponDefs[wdid].name, type = WeaponDefs[wdid].type}
  return c.w[wdid]
end

function gadget:UnitPreDamaged(uid, _, _, damage, _, weaponDefID, _, attacker)
  local c = attacker and byAttacker[attacker]
  if c and weaponDefID and weaponDefID >= 0 and damage > 0 then
    local rec = weaponRec(c, weaponDefID)
    rec.hits = rec.hits + 1
    rec.damage = rec.damage + damage
    rec.victim = rec.victim or UnitDefs[Spring.GetUnitDefID(uid)].name
  end
  return 0, 0
end

local watched = {}
function gadget:ProjectileCreated(pid, owner, weaponDefID)
  local c = owner and byAttacker[owner]
  if not c then return end
  local rec = weaponRec(c, weaponDefID)
  rec.shots = rec.shots + 1
  if rec.shots <= 2 then
    local px, py, pz = Spring.GetProjectilePosition(pid)
    local bx, by, bz = Spring.GetUnitBasePosition(owner)
    local dropX, dropY, dropZ = pieceWorld(owner, Spring.GetUnitPieceMap(owner).bombdrop or 1)
    local vx, vy, vz = Spring.GetProjectileVelocity(pid)
    log("W", c.tag, rec.name, "shot", rec.shots, "at", fmt(px), fmt(py), fmt(pz), "owner", fmt(bx), fmt(by), fmt(bz), "drop piece", fmt(dropX), fmt(dropY), fmt(dropZ), "vel", fmt(vx), fmt(vy), fmt(vz))
    if WeaponDefs[weaponDefID].type == "TorpedoLauncher" then watched[pid] = {tag = c.tag, n = 0} end
  end
end

local function setupWeaponCases()
  for wd = 0, #WeaponDefs do
    if WeaponDefs[wd] then Script.SetWatchProjectile(wd, true) end
  end
  for i, c in ipairs(W_CASES) do
    local x, z = c.x or 7400 + ((i - 1) % 4) * 1400, c.z or 1500 + math.floor((i - 1) / 4) * 3000
    c.tag = string.format("%02d %s>%s(%s)", i, c.a, c.b, c.order)
    c.w, c.slot, c.lastReload = {}, {0, 0, 0}, {0, 0, 0}
    c.uid = Spring.CreateUnit(c.a, x, Spring.GetGroundHeight(x, z), z, 0, TEAM)
    c.target = Spring.CreateUnit(c.b, x, Spring.GetGroundHeight(x, z + 300), z + 300, 0, 0)
    if c.order == "auto" then
      Spring.GiveOrderToUnit(c.uid, CMD.FIRE_STATE, {2}, {})
    else
      Spring.GiveOrderToUnit(c.uid, CMD.ATTACK, {c.target}, {})
    end
    Spring.GiveOrderToUnit(c.target, CMD.FIRE_STATE, {0}, {})
    if c.circle then
      Spring.GiveOrderToUnit(c.target, CMD.MOVE, {x + 300, 0, z + 300}, {})
      Spring.GiveOrderToUnit(c.target, CMD.MOVE, {x - 300, 0, z + 300}, {"shift"})
      Spring.GiveOrderToUnit(c.target, CMD.MOVE, {x, 0, z - 300}, {"shift"})
      Spring.GiveOrderToUnit(c.target, CMD.REPEAT, {1}, {})
    end
    if c.visible then Spring.SetUnitAlwaysVisible(c.target, true) end   -- its attack runs otherwise overshoot its sight and the order ends
    if c.sonar then Spring.SetUnitSensorRadius(c.uid, "sonar", 2000) end
    byAttacker[c.uid] = c
  end
end

local function reportWeapons()
  for _, c in ipairs(W_CASES) do
    local ud = UnitDefs[Spring.GetUnitDefID(c.uid)]
    local tx, ty, tz = Spring.GetUnitPosition(c.target)
    log("W", c.tag, "target y", fmt(ty))
    for w, wd in ipairs(ud.weapons) do
      local rec = c.w[wd.weaponDef]
      if rec then
        log("W", c.tag, "w" .. w, rec.name, rec.type, "reloads in this slot", c.slot[w], "def total shots", rec.shots, "hits", rec.hits, "damage", fmt(rec.damage), "victim", tostring(rec.victim))
      else
        log("W", c.tag, "w" .. w, WeaponDefs[wd.weaponDef].name, "NO SHOTS")
      end
    end
  end
end

-- what: "unit" = LOAD_UNITS on the id; "area" = LOAD_UNITS on a circle round the cargo
local CASES = {
  {t = "arm_t1_hov_bear",     c = "arm_t1_bot_peewee",  tx = 6400, cx = 6200, what = "unit"},
  {t = "arm_t1_hov_bear",     c = "arm_t1_bot_peewee",  tx = 6400, cx = 6200, what = "area"},
  {t = "arm_t1_hov_bear",     c = "arm_t1_hov_skimmer", tx = 6400, cx = 6350, what = "unit"},
  {t = "arm_t1_hov_bear",     c = "arm_t1_bot_peewee",  tx = 5000, cx = 5100, what = "unit"},   -- both on land, what two older probes tried
  {t = "core_t1_hov_turtle",  c = "arm_t1_bot_peewee",  tx = 6400, cx = 6200, what = "unit"},
  {t = "core_t1_hov_turtle",  c = "arm_t1_bot_peewee",  tx = 6400, cx = 6200, what = "area"},
  {t = "core_t1_hov_turtle",  c = "arm_t1_hov_skimmer", tx = 6400, cx = 6350, what = "unit"},
  {t = "core_t1_hov_turtle",  c = "arm_t1_bot_peewee",  tx = 5000, cx = 5100, what = "unit"},
  {t = "arm_t1_sea_hulk",     c = "arm_t1_bot_peewee",  tx = 6450, cx = 6200, what = "unit"},
  {t = "arm_t1_sea_hulk",     c = "arm_t1_bot_peewee",  tx = 6450, cx = 6200, what = "area"},
  {t = "arm_t1_sea_hulk",     c = "arm_t1_hov_skimmer", tx = 6450, cx = 6350, what = "unit"},
  {t = "arm_t1_sea_hulk",     c = "arm_t1_bot_peewee",  tx = 6500, cx = 5900, what = "unit"},   -- out of reach of the shore
  {t = "core_t1_sea_envoy",   c = "arm_t1_bot_peewee",  tx = 6450, cx = 6200, what = "unit"},
  {t = "core_t1_sea_envoy",   c = "arm_t1_bot_peewee",  tx = 6450, cx = 6200, what = "area"},
  {t = "core_t1_sea_envoy",   c = "arm_t1_hov_skimmer", tx = 6450, cx = 6350, what = "unit"},
  {t = "arm_t1_air_atlas",    c = "arm_t1_bot_peewee",  tx = 6100, cx = 6000, what = "unit"},   -- control
}

local function cmdQueue(uid)
  local q = Spring.GetUnitCommands(uid, 3) or {}
  local s = {}
  for i, c in ipairs(q) do s[i] = tostring(c.id) .. "/" .. #c.params end
  return "[" .. table.concat(s, " ") .. "]"
end

local function cmdSpot(uid)
  local q = Spring.GetUnitCommands(uid, 1) or {}
  local p = q[1] and q[1].params or {}
  local m = Spring.GetUnitMoveTypeData(uid) or {}
  return string.format("spot %s,%s movetype goal %s,%s progress %s", fmt(p[1]), fmt(p[3]), fmt(m.goalx), fmt(m.goalz), tostring(m.progressState))
end

local function spawn(name, x, z)
  return Spring.CreateUnit(name, x, Spring.GetGroundHeight(x, z), z, 0, TEAM)
end

local function setup(i, cs)
  cs.z = 300 + (i - 1) * 700
  cs.tag = string.format("%02d %s<-%s(%s)", i, cs.t, cs.c, cs.what)
  cs.uid = spawn(cs.t, cs.tx, cs.z)
  cs.cargo = spawn(cs.c, cs.cx, cs.z)
  if not cs.uid or not cs.cargo then log(cs.tag, "SPAWN FAIL") cs.dead = true return end
  local ud, cd = UnitDefs[Spring.GetUnitDefID(cs.uid)], UnitDefs[Spring.GetUnitDefID(cs.cargo)]
  log(cs.tag, "rules: isTransport", tostring(ud.isTransport), "size", ud.transportSize, "cap", ud.transportCapacity, "mass", ud.transportMass,
    "radius", ud.loadingRadius, "| cargo xsize", cd.xsize, "mass", cd.mass, "cantBeTransported", tostring(cd.cantBeTransported),
    "ground", fmt(Spring.GetGroundHeight(cs.tx, cs.z)), fmt(Spring.GetGroundHeight(cs.cx, cs.z)))
end

local function step(cs, f)
  if cs.dead or not Spring.ValidUnitID(cs.uid) or not Spring.ValidUnitID(cs.cargo) then return end
  local x, y, z = Spring.GetUnitPosition(cs.uid)
  local cx, cy, cz = Spring.GetUnitPosition(cs.cargo)
  local d2 = math.sqrt((x - cx) ^ 2 + (z - cz) ^ 2)
  local carrying = #(Spring.GetUnitIsTransporting(cs.uid) or {})
  local st = cs.state or "wait"
  if st == "wait" then
    if f >= 90 then
      if cs.what == "unit" then
        Spring.GiveOrderToUnit(cs.uid, CMD.LOAD_UNITS, {cs.cargo}, {})
      else
        Spring.GiveOrderToUnit(cs.uid, CMD.LOAD_UNITS, {cx, cy, cz, 100}, {})
      end
      cs.state, cs.t0 = "load", f
      log(cs.tag, "order given, queue", cmdQueue(cs.uid))
    end
  elseif st == "load" then
    if (f - cs.t0) % 90 == 0 or carrying > 0 then
      log(cs.tag, "load +" .. (f - cs.t0), "carrying", carrying, "dist2d", fmt(d2), "t", fmt(x), fmt(y), "c", fmt(cx), fmt(cy), "queue", cmdQueue(cs.uid))
    end
    if carrying > 0 then
      if cs.px then
        log(cs.tag, "attach snap: cargo was", fmt(cs.px), fmt(cs.py), fmt(cs.pz), "now", fmt(cx), fmt(cy), fmt(cz), "jump x", fmt(cx - cs.px), "y", fmt(cy - cs.py), "z", fmt(cz - cs.pz))
      end
      cs.state, cs.t0 = "lifting", f
    elseif f - cs.t0 > 1500 then
      log(cs.tag, "NEVER LOADED")
      cs.state = "done"
    end
    cs.px, cs.py, cs.pz = cx, cy, cz
  elseif st == "lifting" then
    local q = Spring.GetUnitCommands(cs.uid, 1) or {}
    if (f - cs.t0) % 30 == 0 then
      log(cs.tag, "lift +" .. (f - cs.t0), "cargo offset", fmt(cx - x), fmt(cy - y), fmt(cz - z), "queue", cmdQueue(cs.uid))
    end
    if #q == 0 and f - cs.t0 > 30 then
      log(cs.tag, "stowed after", f - cs.t0, "frames, cargo offset", fmt(cx - x), fmt(cy - y), fmt(cz - z),
        "transporter", tostring((Spring.GetUnitTransporter(cs.cargo))))
      Spring.GiveOrderToUnit(cs.uid, CMD.MOVE, {x, y, z + 300}, {})
      cs.state, cs.t0, cs.x0, cs.z0 = "moving", f, x, z
    elseif f - cs.t0 > 900 then
      log(cs.tag, "STILL BUSY after 900 frames")
      cs.state = "done"
    end
  elseif st == "moving" then
    if (f - cs.t0) % 40 == 0 then
      log(cs.tag, "moving +" .. (f - cs.t0), "t moved", fmt(z - cs.z0), "cargo offset", fmt(cx - x), fmt(cy - y), fmt(cz - z), "speed", fmt(select(4, Spring.GetUnitVelocity(cs.uid))))
    end
    if f - cs.t0 >= 360 then
      local ux, uz = cs.cx, z
      cs.ux, cs.uz = ux, uz
      Spring.GiveOrderToUnit(cs.uid, CMD.UNLOAD_UNITS, {ux, Spring.GetGroundHeight(ux, uz), uz, 80}, {})
      cs.state, cs.t0 = "unload", f
      log(cs.tag, "unload ordered at", ux, uz, "queue", cmdQueue(cs.uid))
    end
  elseif st == "unload" then
    if (f - cs.t0) % 90 == 0 then
      log(cs.tag, "unload +" .. (f - cs.t0), "carrying", carrying, "t", fmt(x), fmt(y), "c", fmt(cx), fmt(cy), fmt(cz), "queue", cmdQueue(cs.uid), cmdSpot(cs.uid))
    end
    if carrying == 0 and #(Spring.GetUnitCommands(cs.uid, 1) or {}) == 0 then
      log(cs.tag, "UNLOADED: cargo at", fmt(cx), fmt(cy), fmt(cz), "ground", fmt(Spring.GetGroundHeight(cx, cz)), "cargo transporter", tostring((Spring.GetUnitTransporter(cs.cargo))))
      cs.state = "done"
    elseif f - cs.t0 > 1200 then
      log(cs.tag, "NEVER UNLOADED, carrying", carrying)
      cs.state = "done"
    end
  end
end

function gadget:UnitUnloaded(uid, _, _, transportID)
  for _, cs in ipairs(CASES) do
    if cs.cargo == uid then
      local x, y, z = Spring.GetUnitPosition(uid)
      log(cs.tag, "detached at", fmt(x), fmt(y), fmt(z), "ground", fmt(Spring.GetGroundHeight(x, z)), "from wanted", fmt(cs.ux), fmt(cs.uz), "off", fmt(math.sqrt((x - (cs.ux or 0)) ^ 2 + (z - (cs.uz or 0)) ^ 2)))
    end
  end
end

function gadget:GameFrame(f)
  if f == 1 then Spring.SendCommands("cheat 1", "setmaxspeed 200", "setminspeed 200") end
  if f == 30 then
    for i, cs in ipairs(CASES) do setup(i, cs) end
    Spring.CreateUnit("arm_t1_bot_peewee", 100, 0, SIZEZ - 100, 0, 0)    -- keeps team 0 alive whatever happens
    setupWeaponCases()
    Spring.SetTeamResource(TEAM, "metal", 100000)
  end
  if f < 60 then return end
  for pid, w in pairs(watched) do
    w.n = w.n + 1
    local px, py, pz = Spring.GetProjectilePosition(pid)
    if not px then
      watched[pid] = nil
    elseif w.n % 15 == 0 then
      log("W", w.tag, "torpedo", pid, "+" .. w.n, "at", fmt(px), fmt(py), fmt(pz))
    end
  end
  if f == W_FRAME0 + W_FRAMES then reportWeapons() end
  for _, c in ipairs(W_CASES) do      -- both of the Archer's missile slots share a weapon def, so count launches per slot
    for w = 1, 3 do
      local r = c.uid and Spring.ValidUnitID(c.uid) and Spring.GetUnitWeaponState(c.uid, w, "reloadFrame")
      if r and r > f and r ~= c.lastReload[w] then c.slot[w] = c.slot[w] + 1 end
      if r then c.lastReload[w] = r end
    end
  end
  if f % 120 == 0 then
    for _, c in ipairs(W_CASES) do
      if c.a:find("typhoon") and c.uid and Spring.ValidUnitID(c.uid) then
        local x, y, z = Spring.GetUnitPosition(c.uid)
        local tx, ty, tz = Spring.GetUnitPosition(c.target)
        local parts = {}
        for w = 1, 3 do
          parts[w] = string.format("w%d reload %d range %s los %s", w, Spring.GetUnitWeaponState(c.uid, w, "reloadFrame") or -1,
            tostring(Spring.GetUnitWeaponTestRange(c.uid, w, c.target)), tostring(Spring.GetUnitWeaponTestTarget(c.uid, w, c.target)))
        end
        log("W", c.tag, "f", f, "plane", fmt(x), fmt(y), fmt(z), "dist", fmt(math.sqrt((x-tx)^2+(z-tz)^2)), "queue", cmdQueue(c.uid), table.concat(parts, "; "))
      end
    end
  end
  local busy = f <= W_FRAME0 + W_FRAMES
  for _, cs in ipairs(CASES) do
    step(cs, f)
    if not cs.dead and cs.state ~= "done" then busy = true end
  end
  if (not busy and f > 200) or f > 6000 then
    log("end frame", f)
    Spring.SendCommands("quitforce")
  end
end
