function gadget:GetInfo()
  return { name = "Script Probe", layer = 1004, enabled = true }
end

-- Exercises what zz_walker_aim_probe does not, for COB and Lua alike (SCRIPTP=1 run.sh), logging [SP] lines for tools/s3okit/kit/compare_probe.py to diff:
-- every unit def on its own cell (lake for water units): piece poses idle, with on/off toggled, moving (twice 10 frames apart: spinners show up as a
-- difference), the corpse at low and high death severity, factories (build, yard open, stance, finished unit), builders (a nanoframe gets built),
-- transports, air repair pads, stockpile weapons, and resource rates.
if not gadgetHandler:IsSyncedCode() or not (Spring.GetModOptions() or {}).scriptonly then return end

local SIZE = Game.mapSizeX
local LAKE_X0, LAKE_X1 = SIZE * 0.55, SIZE * 0.97
local CELL = 240
local units, byUid = {}, {}
local immune = {}

local function log(...) Spring.Echo("[SP]", ...) end

function gadget:Initialize()
  Spring.SetHeightMapFunc(function()
    for x = 0, SIZE, 8 do
      for z = 0, Game.mapSizeZ, 8 do
        if x > LAKE_X0 and x < LAKE_X1 then Spring.SetHeightMap(x, z, -60) end
      end
    end
  end)
end

function gadget:UnitPreDamaged(uid, _, _, damage)
  if immune[uid] then return 0, 0 end
end

local function isWaterUnit(ud)
  if ud.minWaterDepth and ud.minWaterDepth > 0 then return true end
  local md = ud.moveDef
  local n = md and md.name and md.name:lower() or ""
  return n:find("ship") ~= nil or n:find("boat") ~= nil or n:find("sub") ~= nil
end

local function logPose(uid, name, tag)
  local names = Spring.GetUnitPieceList(uid)
  if not names then return end
  local parts = {}
  for i, n in ipairs(names) do
    local m = {Spring.GetUnitPieceMatrix(uid, i)}
    parts[#parts + 1] = string.format("%s=%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.1f,%.1f,%.1f", n, m[1], m[2], m[3], m[5], m[6], m[7], m[9], m[10], m[11], m[13], m[14], m[15])
  end
  Spring.Echo("[POSE] " .. name .. " " .. tag .. " " .. table.concat(parts, " "))
end

local P = {IDLE = 120, ON = 300, OFF = 420, OFF2 = 700, MOVE1 = 1000, MOVE2 = 1010, STOP = 1200, HITLOW = 1500, HITHIGH = 1560, END = 1700}
local spawnFrame = 30
local corpseOf = {}
local dying = {}

function gadget:FeatureCreated(fid)
  local x, _, z = Spring.GetFeaturePosition(fid)
  local name = FeatureDefs[Spring.GetFeatureDefID(fid)].name
  local best, bd = nil, 150
  for uid, s in pairs(dying) do
    local d = math.max(math.abs(s.dx - x), math.abs(s.dz - z))
    if d < bd then best, bd = s, d end
  end
  if best then log("corpse", best.name, best.sev, name) ; dying[best.uid] = nil end
end

-- ---- factories / builders
local built = {}
function gadget:UnitCreated(uid, udid, team, builder)
  if builder and byUid[builder] then
    local s = byUid[builder]
    s.building = uid
    s.buildName = UnitDefs[udid].name
    immune[uid] = true
  end
end
function gadget:UnitFinished(uid, udid)
  for _, s in ipairs(units) do
    if s.building == uid then s.finished = Spring.GetGameFrame() end
  end
end

-- ---- specials
local specials = {}
local function spawnSpecial(name, x, z, team)
  local uid = Spring.CreateUnit(name, x, Spring.GetGroundHeight(x, z), z, 0, team or 1)
  if uid then immune[uid] = true end
  return uid
end

local function setup(frame)
  for t = 0, 1 do
    Spring.SetTeamResource(t, "es", 1e8) ; Spring.SetTeamResource(t, "e", 1e8)
    Spring.SetTeamResource(t, "ms", 1e8) ; Spring.SetTeamResource(t, "m", 1e8)
  end
  Spring.CreateUnit("arm_t1_bot_peewee", 100, 0, Game.mapSizeZ - 100, 0, 0)
  local ids = {}
  for id in pairs(UnitDefs) do ids[#ids + 1] = id end
  table.sort(ids)
  local nLand, nSea = 0, 0
  local landCols, seaCols = math.floor(LAKE_X0 / CELL) - 1, math.floor((LAKE_X1 - LAKE_X0) / CELL) - 1
  for _, id in ipairs(ids) do
    local ud = UnitDefs[id]
    local sea = isWaterUnit(ud)
    local x, z
    if sea then
      x, z = LAKE_X0 + 300 + (nSea % seaCols) * CELL, 300 + math.floor(nSea / seaCols) * CELL
      nSea = nSea + 1
    else
      x, z = 300 + (nLand % landCols) * CELL, 300 + math.floor(nLand / landCols) * CELL
      nLand = nLand + 1
    end
    local uid = Spring.CreateUnit(id, x, Spring.GetGroundHeight(x, z), z, 0, 1)
    if uid then
      immune[uid] = true
      local s = {uid = uid, name = ud.name, ud = ud, x = x, z = z}
      units[#units + 1] = s
      byUid[uid] = s
      Spring.GiveOrderToUnit(uid, CMD.FIRE_STATE, {0}, {})
    else
      log("spawn failed", ud.name)
    end
  end
  -- transports: x = 300 + ..., south part of the land side
  local tz = Game.mapSizeZ - 900
  local function transportTest(tname, cargo, x, z, sea)
    local t = spawnSpecial(tname, x, z)
    local c = spawnSpecial(cargo, x + 80, z)
    if t and c then specials[#specials + 1] = {kind = "transport", name = tname, t = t, c = c, x = x, z = z, sea = sea} end
  end
  transportTest("arm_t1_air_atlas", "arm_t1_bot_peewee", 300, tz)
  transportTest("core_t1_air_valkyrie", "arm_t1_bot_peewee", 900, tz)
  transportTest("arm_t1_hov_bear", "arm_t1_bot_peewee", 1500, tz)
  transportTest("core_t1_hov_turtle", "arm_t1_bot_peewee", 2100, tz)
  transportTest("arm_t1_sea_hulk", "arm_t1_hov_skimmer", LAKE_X0 + 300, tz, true)
  transportTest("core_t1_sea_envoy", "arm_t1_hov_skimmer", LAKE_X0 + 900, tz, true)
  -- repair pads
  local rz = Game.mapSizeZ - 500
  for i, pad in ipairs({"arm_t2_def_airrepairpad", "core_t2_def_airrepairpad"}) do
    local x = 300 + (i - 1) * 600
    local p = spawnSpecial(pad, x, rz)
    local a = spawnSpecial(i == 1 and "arm_t1_air_thunder" or "core_t1_air_shadow", x + 150, rz)
    if p and a then specials[#specials + 1] = {kind = "pad", name = pad, p = p, a = a} end
  end
  for i, pad in ipairs({"arm_t2_sea_colossus", "core_t2_sea_hive"}) do
    local x = LAKE_X0 + 300 + (i - 1) * 700
    local p = spawnSpecial(pad, x, rz)
    local a = spawnSpecial(i == 1 and "arm_t1_air_thunder" or "core_t1_air_shadow", x + 150, rz)
    if p and a then specials[#specials + 1] = {kind = "pad", name = pad, p = p, a = a} end
  end
  -- stockpile weapons
  local sz = Game.mapSizeZ - 1500
  for i, name in ipairs({"arm_t2_def_retaliator", "core_t2_def_silencer", "arm_t2_veh_scarab"}) do
    local x = 300 + (i - 1) * 2200
    local u = spawnSpecial(name, x, sz)
    local tgt = spawnSpecial("arm_t1_bot_peewee", x + 700, sz, 0)
    if u then specials[#specials + 1] = {kind = "stock", name = name, u = u, tgt = tgt, x = x, z = sz} end
  end
  local fort = spawnSpecial("core_t2_def_fortitudemissiledefense", 300 + 2200 * 3, sz)
  if fort then specials[#specials + 1] = {kind = "stockdef", name = "core_t2_def_fortitudemissiledefense", u = fort} end
  log("spawned", #units)
end

local function value(uid, v) return Spring.GetUnitCOBValue(uid, v) end
local function resources(uid)
  local mm, mu, em, eu = Spring.GetUnitResources(uid)
  return string.format("%.2f %.2f %.2f %.2f", mm or 0, mu or 0, em or 0, eu or 0)
end

local function eachUnit(fn)
  for _, s in ipairs(units) do
    if Spring.ValidUnitID(s.uid) then fn(s) end
  end
end

local started = false
function gadget:GameFrame(frame)
  if frame == spawnFrame then setup(frame); started = true; return end
  if not started then return end
  local f = frame - spawnFrame
  if f == P.IDLE then
    eachUnit(function(s)
      logPose(s.uid, s.name, "idle")
      log("state", s.name, "idle", "act", value(s.uid, COB.ACTIVATION), "armored", tostring(select(1, Spring.GetUnitArmored(s.uid))), "res", resources(s.uid))
      Spring.GiveOrderToUnit(s.uid, CMD.ONOFF, {1}, {})
    end)
  elseif f == P.ON then
    eachUnit(function(s)
      logPose(s.uid, s.name, "on")
      log("state", s.name, "on", "act", value(s.uid, COB.ACTIVATION), "armored", tostring(select(1, Spring.GetUnitArmored(s.uid))), "res", resources(s.uid))
      Spring.GiveOrderToUnit(s.uid, CMD.ONOFF, {0}, {})
    end)
  elseif f == P.OFF then
    eachUnit(function(s) logPose(s.uid, s.name, "off1") end)
  elseif f == P.OFF2 then
    eachUnit(function(s)
      logPose(s.uid, s.name, "off")
      log("state", s.name, "off", "act", value(s.uid, COB.ACTIVATION), "armored", tostring(select(1, Spring.GetUnitArmored(s.uid))), "res", resources(s.uid))
      Spring.GiveOrderToUnit(s.uid, CMD.ONOFF, {1}, {})
      local ud = s.ud
      if ud.isFactory and ud.buildOptions[1] then
        Spring.GiveOrderToUnit(s.uid, -ud.buildOptions[1], {}, {})
      elseif ud.isBuilder and ud.buildOptions[1] and ud.canMove then
        local x, y, z = Spring.GetUnitPosition(s.uid)
        Spring.GiveOrderToUnit(s.uid, -ud.buildOptions[1], {x + 60, y, z + 60, 0}, {})
      elseif ud.canMove then
        Spring.GiveOrderToUnit(s.uid, CMD.MOVE, {s.x + 90, 0, s.z + 90}, {})
      end
    end)
  elseif f == P.OFF2 + 100 then
    eachUnit(function(s)
      if s.ud.isFactory then
        log("factory", s.name, "t100 yard", value(s.uid, COB.YARD_OPEN), "stance", value(s.uid, COB.INBUILDSTANCE), "busy", value(s.uid, COB.BUSY), "building", tostring(s.buildName))
      end
    end)
  elseif f == P.MOVE1 then
    eachUnit(function(s) if s.ud.canMove then logPose(s.uid, s.name, "move1") end end)
  elseif f == P.MOVE2 then
    eachUnit(function(s) if s.ud.canMove then logPose(s.uid, s.name, "move2") end end)
  elseif f == P.STOP then
    eachUnit(function(s)
      if s.ud.isFactory then
        local b = s.building
        local prog = b and Spring.ValidUnitID(b) and select(5, Spring.GetUnitHealth(b)) or -1
        log("factory", s.name, "t500 yard", value(s.uid, COB.YARD_OPEN), "stance", value(s.uid, COB.INBUILDSTANCE), "building", tostring(s.buildName), "progress>0", tostring(prog > 0), "buildinfo", tostring(b and Spring.ValidUnitID(b)))
      elseif s.ud.isBuilder and s.ud.canMove then
        local b = s.building
        local prog = b and Spring.ValidUnitID(b) and select(5, Spring.GetUnitHealth(b)) or -1
        log("builder", s.name, "building", tostring(s.buildName), "progress>0", tostring(prog > 0))
      end
      if s.ud.canMove then Spring.GiveOrderToUnit(s.uid, CMD.STOP, {}, {}) end
    end)
  elseif f == P.STOP + 150 then
    eachUnit(function(s) if s.ud.canMove then logPose(s.uid, s.name, "stopped") end end)
  elseif f == P.HITLOW then
    -- severity 20: wreck level for a light death
    eachUnit(function(s)
      if s.name then
        immune[s.uid] = nil
        local x, _, z = Spring.GetUnitPosition(s.uid)
        s.dx, s.dz, s.sev = x, z, 20
        dying[s.uid] = s
        local _, maxh = Spring.GetUnitHealth(s.uid)
        Spring.SetUnitHealth(s.uid, 1)
        Spring.AddUnitDamage(s.uid, maxh * 0.2)
      end
    end)
  elseif f == P.HITHIGH then
    -- severity over 100: the same again with a fresh copy
    for _, s in ipairs(units) do
      local uid = Spring.CreateUnit(s.ud.id, s.x, Spring.GetGroundHeight(s.x, s.z), s.z, 0, 1)
      if uid then
        local copy = {uid = uid, name = s.name, dx = s.x, dz = s.z, sev = 120}
        dying[uid] = copy
        local _, maxh = Spring.GetUnitHealth(uid)
        Spring.SetUnitHealth(uid, 1)
        Spring.AddUnitDamage(uid, maxh * 1.2)
      end
    end
  elseif f == P.END then
    log("DONE")
    Spring.SendCommands("quitforce")
  end

  -- specials timeline
  for _, sp in ipairs(specials) do
    if sp.kind == "transport" then
      if f == 150 then Spring.GiveOrderToUnit(sp.t, CMD.LOAD_UNITS, {sp.c}, {}) end
      if f == 600 then
        local cargo = Spring.GetUnitIsTransporting(sp.t) or {}
        log("transport", sp.name, "loaded", #cargo)
        logPose(sp.t, sp.name, "tload")
        local x, y, z = Spring.GetUnitPosition(sp.t)
        Spring.GiveOrderToUnit(sp.t, CMD.UNLOAD_UNIT, {x + 120, y, z + 120}, {})
      end
      if f == 1100 then
        local cargo = Spring.GetUnitIsTransporting(sp.t) or {}
        log("transport", sp.name, "after unload", #cargo)
      end
    elseif sp.kind == "pad" then
      if f == 150 then
        Spring.SetUnitHealth(sp.a, select(2, Spring.GetUnitHealth(sp.a)) * 0.3)
        Spring.GiveOrderToUnit(sp.a, CMD.MOVE, {Spring.GetUnitPosition(sp.p)}, {})
        Spring.GiveOrderToUnit(sp.a, CMD.AUTOREPAIRLEVEL, {3}, {})
      end
      if f == 200 then
        -- this engine has no air bases left (no caller of QueryLandingPads): just check the script's answer
        local env = Spring.UnitScript.GetScriptEnv(sp.p)
        if env and env.script.QueryLandingPads then
          local r = Spring.UnitScript.CallAsUnit(sp.p, env.script.QueryLandingPads)
          local list = Spring.GetUnitPieceList(sp.p)
          local names = {}
          for i, q in ipairs(r or {}) do names[i] = tostring(list[q]) end
          Spring.Echo("[SPLUA] pads", sp.name, table.concat(names, " "))
        end
      end
      if f == 1100 then
        local h, m = Spring.GetUnitHealth(sp.a)
        log("pad", sp.name, "aircraft health frac", string.format("%.2f", h / m), "pad transporter", tostring((Spring.GetUnitTransporter(sp.a))))
      end
    elseif sp.kind == "stock" then
      if f == 150 then
        Spring.SetUnitStockpile(sp.u, 3)
        Spring.GiveOrderToUnit(sp.u, CMD.ATTACK, {sp.x + 700, Spring.GetGroundHeight(sp.x + 700, sp.z), sp.z}, {})
        sp.left = 3
      end
      if f > 150 and f == 1100 then
        local n = Spring.GetUnitStockpile(sp.u)
        log("stock", sp.name, "stockpile after attack", tostring(n))
      end
    elseif sp.kind == "stockdef" then
      if f == 150 then Spring.SetUnitStockpile(sp.u, 3) end
      if f == 1100 then log("stock", sp.name, "interceptor stockpile", tostring(Spring.GetUnitStockpile(sp.u))) end
    end
  end
end
