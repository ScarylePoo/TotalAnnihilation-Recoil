function gadget:GetInfo()
  return { name = "Piece Gap Probe", layer = 1004, enabled = true }
end

-- Do pieces stay attached to the unit while it animates? Runs alone (GAP=1 run.sh). Spawns one immune copy of EVERY unit def on team 1, each in its own cell
-- (water units in the harness's lake) and walks it through idle, off, on, ground attacks far and near, attack on an enemy (land, ship or aircraft to suit
-- the weapon), manual fire, a direct call of the aim and fire scripts (interceptors and stockpile weapons never aim on their own, nothing here launches a nuke), move out and back, build (builders and factories; products are removed), stop, load and unload (transports). Every SAMPLE frames each unit's piece
-- matrices (Spring.GetUnitPieceMatrix, model space) go to the infolog as GAPD lines (synced Lua has no io), skipping pieces that did not change; run.sh
-- extracts them to gapdata.txt and tools/s3okit/kit/piece_gaps.py poses the real S3O geometry from them.
-- The engine has no visibility query (Spring.UnitScript has no getter), so Hide/Show are wrapped here: unit_script_header.lua reads them from Spring.UnitScript
-- when each unit's script chunk runs, so LUS units report the truth. COB units cannot be wrapped; piece_gaps.py reads their hide/show from the bytecode.
-- Format, ';' separated records: "U id name model" / "P id idx name parent" / "F frame phase" (phase starts) / "S id frame" then "M idx vis 12 numbers"
-- (3x3 by columns, then translation) / "D id frame" (died).
local opt = Spring.GetModOptions() or {}
if not opt.gaponly then return end

if gadgetHandler:IsSyncedCode() then

local SAMPLE = 4
local PHASES = {  -- name, duration in frames
  {"idle", 90}, {"off", 150}, {"on", 150}, {"attackfar", 330}, {"attacknear", 330}, {"attackunit", 300}, {"manual", 180},
  {"aimdirect", 300},
  {"move", 330}, {"halt", 150}, {"build", 480}, {"stop", 240}, {"load", 300}, {"unload", 300},
}
local SIZE = Game.mapSizeX
local LAKE_X0, LAKE_X1 = SIZE * 0.55, SIZE * 0.95
local CELL = 420
local units, protected = {}, {}
local hidden = {}   -- hidden[unitID][piece] = true

local US = Spring.UnitScript
local function wrapVis(name, value)
  local orig = US[name]
  US[name] = function(p, ...)
    local uid = US.GetActiveUnitID()
    if uid then
      hidden[uid] = hidden[uid] or {}
      hidden[uid][p] = value or nil
    end
    return orig(p, ...)
  end
end
wrapVis("Hide", true)
wrapVis("Show", false)

local buf, bufN = {}, 0
local function flush()
  if bufN > 0 then
    Spring.Echo("GAPD " .. table.concat(buf, ";"))
    buf, bufN = {}, 0
  end
end
local function emit(line)
  if bufN + #line > 900 then flush() end
  buf[#buf + 1] = line
  bufN = bufN + #line + 1
end

local function log(...) Spring.Echo("[HARNESS] gap", ...) end

function gadget:Initialize()
  Spring.SetHeightMapFunc(function()
    for x = 0, SIZE, 8 do
      for z = 0, Game.mapSizeZ, 8 do
        if x > LAKE_X0 and x < LAKE_X1 then Spring.SetHeightMap(x, z, -60) end
      end
    end
  end)
end

function gadget:UnitPreDamaged(uid)
  if protected[uid] then return 0, 0 end
end

local function isWaterUnit(ud)
  if ud.minWaterDepth and ud.minWaterDepth > 0 then return true end
  local md = ud.moveDef
  local n = md and md.name and md.name:lower() or ""
  return (n:find("ship") or n:find("boat") or n:find("sub")) and true or false
end

local function hold(uid)
  if uid then
    protected[uid] = true
    Spring.GiveOrderToUnit(uid, CMD.FIRE_STATE, {0}, {})
    Spring.GiveOrderToUnit(uid, CMD.MOVE_STATE, {0}, {})
  end
  return uid
end

-- the enemy this def's weapons can actually shoot
local function makeTarget(s, ud)
  local aaOnly, waterOnly, armed = true, true, false
  for _, wd in ipairs(ud.weapons or {}) do
    local def = WeaponDefs[wd.weaponDef]
    if def and def.range and def.range > 0 and def.name ~= "noweapon" then
      armed = true
      local ot = wd.onlyTargets or {}
      if not (ot.vtol and not ot.notair) then aaOnly = false end
      if not def.waterWeapon then waterOnly = false end
      s.rmin = math.min(s.rmin or 1e9, def.range)
      if def.stockpile then s.stock = true end
      if def.manualFire then s.manual = true end
    end
  end
  s.armed = armed
  if not armed then return end
  s.far, s.near = math.min(s.rmin * 0.7, 180), math.max(math.min(s.rmin * 0.3, 60), 30)
  local tx, tz = s.x, s.z + s.far
  local name = "arm_t1_bot_peewee"
  if aaOnly then name = "arm_t1_air_peeper" elseif waterOnly or s.water then name = "arm_t1_sea_skeeter" end
  s.targetName = name
  if UnitDefNames[name] then
    s.target = hold(Spring.CreateUnit(name, tx, Spring.GetGroundHeight(tx, tz), tz, 0, 0))
  end
end

local landI, seaI = 0, 0
local function spawnAll()
  Spring.SetTeamResource(1, "es", 1e8) ; Spring.SetTeamResource(1, "e", 1e8)
  Spring.SetTeamResource(1, "ms", 1e8) ; Spring.SetTeamResource(1, "m", 1e8)
  Spring.CreateUnit("arm_t1_bot_peewee", 60, 0, Game.mapSizeZ - 60, 0, 0)    -- keeps team 0 alive
  local landCols = math.floor((LAKE_X0 - 400) / CELL)
  local seaCols = math.floor((LAKE_X1 - LAKE_X0 - 400) / CELL)
  local ids = {}
  for id in pairs(UnitDefs) do ids[#ids + 1] = id end
  table.sort(ids)
  for _, id in ipairs(ids) do
    local ud = UnitDefs[id]
    local water = isWaterUnit(ud)
    local x, z
    if water then
      x, z = LAKE_X0 + 250 + (seaI % seaCols) * CELL, 300 + math.floor(seaI / seaCols) * CELL
      seaI = seaI + 1
    else
      x, z = 250 + (landI % landCols) * CELL, 300 + math.floor(landI / landCols) * CELL
      landI = landI + 1
    end
    local ok, uid = pcall(Spring.CreateUnit, id, x, Spring.GetGroundHeight(x, z), z, 0, 1)
    if ok and uid then
      protected[uid] = true
      local s = {uid = uid, ud = ud, x = x, z = z, water = water, last = {}, name = ud.name}
      s.pieces = Spring.GetUnitPieceList(uid) or {}
      emit("U " .. uid .. " " .. ud.name .. " " .. tostring(ud.modelname or (ud.model and ud.model.path) or (ud.model and ud.model.name) or "?"))
      for i, name in ipairs(s.pieces) do
        local info = Spring.GetUnitPieceInfo(uid, i)
        emit("P " .. uid .. " " .. i .. " " .. name .. " " .. tostring(info and info.parent or "-"))
      end
      makeTarget(s, ud)
      units[#units + 1] = s
    else
      log("SPAWN FAIL", ud.name)
    end
  end
  log("subjects", #units, "land", landI, "sea", seaI)
end

local function buildSite(s, opt1)
  for _, d in ipairs({{100, 100}, {-100, 100}, {100, -100}, {-100, -100}, {160, 0}, {-160, 0}}) do
    local x, z = s.x + d[1], s.z + d[2]
    if Spring.TestBuildOrder(opt1, x, Spring.GetGroundHeight(x, z), z, 0) > 0 then return x, z end
  end
end

local function give(uid, c, p, o) Spring.GiveOrderToUnit(uid, c, p, o or {}) end

local enter = {}
function enter.idle() end
function enter.off(s)  if s.ud.onOffable then give(s.uid, CMD.ONOFF, {0}) end end
function enter.on(s)
  if s.ud.onOffable then give(s.uid, CMD.ONOFF, {1}) end
end
function enter.attackfar(s)
  if not s.armed then return end
  give(s.uid, CMD.FIRE_STATE, {0})
  local x, z = s.x + s.far * 0.5, s.z + s.far * 0.866
  give(s.uid, CMD.ATTACK, {x, Spring.GetGroundHeight(x, z), z})
end
function enter.attacknear(s)
  if not s.armed then return end
  local x, z = s.x - s.near * 0.5, s.z - s.near * 0.866
  give(s.uid, CMD.ATTACK, {x, Spring.GetGroundHeight(x, z), z})
end
function enter.attackunit(s)
  if not s.armed then return end
  give(s.uid, CMD.STOP, {})
  if s.target and Spring.ValidUnitID(s.target) then give(s.uid, CMD.ATTACK, {s.target}) end
end
function enter.manual(s)
  if s.stock then Spring.SetUnitStockpile(s.uid, 3) end
  if not s.armed then return end
  give(s.uid, CMD.STOP, {})
  local x, z = s.x + s.far, s.z - s.far * 0.5
  local y = Spring.GetGroundHeight(x, z)
  if s.manual then give(s.uid, CMD.MANUALFIRE, {x, y, z}) elseif s.stock then give(s.uid, CMD.ATTACK, {x, y, z}) end
end
-- run a script callin on either kind of script; COB names its callins differently
local ORD = {"Primary", "Secondary", "Tertiary"}
local function callScript(s, luaName, cobNames, ...)
  local env = Spring.UnitScript.GetScriptEnv and Spring.UnitScript.GetScriptEnv(s.uid)
  if env and env.script then
    if env.script[luaName] then pcall(Spring.UnitScript.CallAsUnit, s.uid, env.script[luaName], ...) end
  else
    local args = {...}
    for _, n in ipairs(cobNames) do pcall(Spring.CallCOBScript, s.uid, n, 0, unpack(args)) end
  end
end
function enter.aimdirect(s)
  if not s.armed then return end
  give(s.uid, CMD.STOP, {})
  for i = 1, #s.ud.weapons do
    local names = {"AimWeapon" .. i, ORD[i] and ("Aim" .. ORD[i]) or nil}
    local env = Spring.UnitScript.GetScriptEnv and Spring.UnitScript.GetScriptEnv(s.uid)
    if env and env.script then
      if env.script.AimWeapon then
        -- wrapped in a thread by unit_script; it may wait on its own turns
        pcall(Spring.UnitScript.CallAsUnit, s.uid, env.script.AimWeapon, i, 0.8, 0.35)
      end
    else
      for _, n in ipairs(names) do pcall(Spring.CallCOBScript, s.uid, n, 0, 8344, 3650) end
    end
  end
end
function enter.move(s)
  callScript(s, "SetSpeed", {"SetSpeed"}, 1000, 0)   -- extractors spin to the metal under them, and this map has none
  give(s.uid, CMD.STOP, {})
  if s.ud.canMove then
    give(s.uid, CMD.MOVE, {s.x + 170, 0, s.z + 120})
    give(s.uid, CMD.MOVE, {s.x - 170, 0, s.z - 120}, {"shift"})
    give(s.uid, CMD.MOVE, {s.x, 0, s.z}, {"shift"})
  end
end
function enter.halt(s) give(s.uid, CMD.STOP, {}) end
function enter.build(s)
  local bo = s.ud.buildOptions
  if not bo or not bo[1] then return end
  if s.ud.isFactory then
    give(s.uid, -bo[1], {})
    give(s.uid, -(bo[2] or bo[1]), {})
  elseif s.ud.isBuilder then
    for _, b in ipairs(bo) do
      local x, z = buildSite(s, b)
      if x then give(s.uid, -b, {x, Spring.GetGroundHeight(x, z), z, 0}) ; return end
    end
    log("no build site", s.name)
  end
end
function enter.stop(s)
  give(s.uid, CMD.STOP, {})
end
function enter.load(s)
  if not s.ud.isTransport and not (s.ud.transportCapacity and s.ud.transportCapacity > 0) then return end
  local x, z = s.x + 70, s.z + 70
  local cargo = s.water and "arm_t1_hov_skimmer" or "arm_t1_bot_peewee"
  s.cargo = Spring.CreateUnit(cargo, x, Spring.GetGroundHeight(x, z), z, 0, 1)
  if s.cargo then
    protected[s.cargo] = true
    give(s.cargo, CMD.FIRE_STATE, {0})
    give(s.uid, CMD.LOAD_UNITS, {s.cargo})
  else
    log("no cargo", s.name)
  end
end
function enter.unload(s)
  if s.cargo then
    local x, z = s.x - 90, s.z + 60
    give(s.uid, CMD.UNLOAD_UNITS, {x, Spring.GetGroundHeight(x, z), z, 50})
  end
end

-- factory products would clutter the cells (and they are not the subject)
function gadget:UnitFromFactory(uid) Spring.DestroyUnit(uid, false, true) end

local function sampleUnit(s, frame)
  if not Spring.ValidUnitID(s.uid) or Spring.GetUnitIsDead(s.uid) then
    if not s.deadLogged then s.deadLogged = true ; emit("D " .. s.uid .. " " .. frame) end
    return
  end
  local wrote = false
  local hid = hidden[s.uid]
  for i = 1, #s.pieces do
    local a = {Spring.GetUnitPieceMatrix(s.uid, i)}
    local vis = (hid and hid[i]) and 0 or 1
    local l = s.last[i]
    local ch = not l or l[17] ~= vis
    if not ch then
      for k = 1, 11 do if k ~= 4 and k ~= 8 and math.abs(a[k] - l[k]) > 0.0015 then ch = true ; break end end
      if not ch then for k = 13, 15 do if math.abs(a[k] - l[k]) > 0.015 then ch = true ; break end end end
    end
    if ch then
      if not wrote then wrote = true ; emit("S " .. s.uid .. " " .. frame) end
      a[17] = vis
      s.last[i] = a
      emit(string.format("M %d %d %.4f %.4f %.4f %.4f %.4f %.4f %.4f %.4f %.4f %.3f %.3f %.3f", i, vis,
        a[1], a[2], a[3], a[5], a[6], a[7], a[9], a[10], a[11], a[13], a[14], a[15]))
    end
  end
end

local T0 = 30
local curPhase, phaseEnd = 0, 0
function gadget:GameFrame(frame)
  if frame == T0 then
    spawnAll()
    phaseEnd = frame
  end
  if frame < T0 then return end
  if frame >= phaseEnd then
    curPhase = curPhase + 1
    local ph = PHASES[curPhase]
    if not ph then
      flush()
      log("DONE")
      Spring.SendCommands("quitforce")
      return
    end
    phaseEnd = frame + ph[2]
    emit("F " .. frame .. " " .. ph[1])
    Spring.SetTeamResource(1, "es", 1e8) ; Spring.SetTeamResource(1, "e", 1e8)
    Spring.SetTeamResource(1, "ms", 1e8) ; Spring.SetTeamResource(1, "m", 1e8)
    for _, s in ipairs(units) do
      if Spring.ValidUnitID(s.uid) then enter[ph[1]](s) end
    end
  end
  if frame % SAMPLE == 0 or frame == T0 + 1 then
    for _, s in ipairs(units) do sampleUnit(s, frame) end
    flush()
  end
end

else

function gadget:Initialize()
  Spring.SendCommands("cheat 1", "setmaxspeed 200", "setminspeed 200")
end

end
