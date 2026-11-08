function gadget:GetInfo()
  return { name = "Boxart Probe", layer = 1007, enabled = true }
end

-- tools/boxart/run_boxart.sh: stages a commander for box-art style renders. A commander of the chosen side
-- (modoption boxart=arm|core) stands on a flat spot with its base behind it, fires its D-Gun, the game pauses while
-- the shot is in flight, and the camera (FPS mode, free placement) takes one screenshot per preset. Interface hidden.
--   boxpause   frames after the D-Gun shot leaves the barrel to pause (default 4)
--   boxaimx    sideways offset of the D-Gun's aim point, as a share of the distance ahead (default -0.2)
--   boxcams    camera presets, "name:dist:height:side:lookheight/..." (a ; would end the start script line) relative to the commander (front = +z)
--   boxaimcam  aim the D-Gun toward this camera preset, boxaimdeg degrees aside (default 12)
--   boxbuild   the commander builds this (a nanoframe) instead of firing; boxbangle, boxprogress
--   boxsunoff  the scene faces the sun's side, turned this many degrees (default 35)
--   boxlight   arm | core: a lighting preset (see LIGHTS)
--   boxx/boxz  where to stand (default: the flattest dry spot found)
local opt = Spring.GetModOptions() or {}
if not opt.boxart then return end

local SIDE = opt.boxart == "core" and "core" or "arm"
local FIRE_FRAME = 150
local PAUSE_AFTER = tonumber(opt.boxpause) or 4

-- the base behind the commander: { name, dx, dz (negative = behind), facing }
local BASES = {
  arm = {
    buildings = {
      { "arm_t2_eco_fusionpowerplant", -300, -520 }, { "arm_t1_lab_kbotlab", 230, -430 },
      { "arm_t2_lab_advancedvehicleplant", -40, -820 }, { "arm_t2_def_annihilator", 470, -640 },
      { "arm_t1_def_guardian", -520, -330 }, { "arm_t1_def_defender", 330, -250 },
      { "arm_t1_def_llt", -210, -220 }, { "arm_t1_def_llt", 170, -200 }, { "arm_t1_def_radartower", -620, -700 },
      { "arm_t2_def_bigbertha", 120, -1150 }, { "arm_t1_eco_solarcollector", -520, -540 },
      { "arm_t1_eco_solarcollector", -440, -620 }, { "arm_t2_def_protector", -420, -1000 },
      { "arm_t1_eco_windgenerator", 620, -360 }, { "arm_t1_eco_windgenerator", 680, -440 },
    },
    units = {
      { "arm_t2_bot_zeus", -120, -90 }, { "arm_t2_bot_zeus", -190, -140 }, { "arm_t2_bot_zeus", 130, -120 },
      { "arm_t2_veh_bulldog", 260, -330 }, { "arm_t2_veh_bulldog", -330, -380 }, { "arm_t1_bot_hammer", 40, -260 },
      { "arm_t1_bot_peewee", -60, -200 }, { "arm_t1_bot_peewee", 90, -320 }, { "arm_t2_bot_fido", 300, -140 },
    },
    air = { { "arm_t2_air_brawler", -150, -300 }, { "arm_t2_air_brawler", 220, -520 }, { "arm_t2_air_brawler", -380, -700 } },
  },
  core = {
    buildings = {
      { "core_t2_eco_fusionpowerplant", -300, -520 }, { "core_t1_lab_kbotlab", 230, -430 },
      { "core_t2_lab_advancedvehicleplant", -40, -820 }, { "core_t2_def_doomsdaymachine", 470, -620 },
      { "core_t1_def_punisher", -520, -330 }, { "core_t1_def_viper", 330, -250 },
      { "core_t1_def_lightlasertower", -210, -220 }, { "core_t1_def_lightlasertower", 170, -200 },
      { "core_t1_def_radartower", -620, -700 }, { "core_t2_def_intimidator", 120, -1150 },
      { "core_t1_eco_solarcollector", -520, -540 }, { "core_t1_eco_solarcollector", -440, -620 },
      { "core_t2_def_fortitudemissiledefense", -420, -1000 }, { "core_t1_eco_windgenerator", 620, -360 },
      { "core_t1_eco_windgenerator", 680, -440 },
    },
    units = {
      { "core_t2_bot_sumo", -150, -110 }, { "core_t2_bot_pyro", -230, -160 }, { "core_t2_bot_pyro", 140, -120 },
      { "core_t2_veh_goliath", 270, -340 }, { "core_t2_veh_reaper", -330, -380 }, { "core_t1_bot_thud", 40, -260 },
      { "core_t1_bot_ak", -60, -200 }, { "core_t1_bot_ak", 90, -320 }, { "core_t3_bot_krogoth", -40, -560 },
    },
    air = { { "core_t2_air_rapier", -150, -300 }, { "core_t2_air_rapier", 220, -520 }, { "core_t2_air_rapier", -380, -700 } },
  },
}

-- camera presets: dist in front of the commander, height above its feet, sideways offset, height of the look point
local CAMS = {}
for spec in tostring(opt.boxcams or "hero:150:10:70:46/low:115:4:-60:52/wide:330:30:150:60/close:85:22:35:42"):gmatch("[^/]+") do
  local name, d, h, sx, lh = spec:match("([^:]+):([^:]+):([^:]+):([^:]+):([^:]+)")
  if name then CAMS[#CAMS + 1] = { name = name, dist = tonumber(d), height = tonumber(h), side = tonumber(sx), look = tonumber(lh) } end
end

if gadgetHandler:IsSyncedCode() then

local com, cx, cz, setupDone, sunKnown
-- the scene's own axes: f (front, toward the camera) points toward the sun's side, turned boxsunoff degrees (default
-- 35) so the light rakes across; r is right. Local (x, z) -> world: c + x * r + z * f
local fx, fz = 0, 1
local function W(lx, lz)
  return cx + lx * fz + lz * fx, cz - lx * fx + lz * fz
end
local function Facing()
  if math.abs(fx) > math.abs(fz) then return fx > 0 and "east" or "west" end
  return fz > 0 and "south" or "north"
end

function gadget:RecvLuaMsg(msg)
  local sx, sz = msg:match("^boxart_sun:([%-%d%.e]+):([%-%d%.e]+)$")
  if sx and not setupDone then
    sx, sz = tonumber(sx), tonumber(sz)
    local a = math.atan2(sx, sz) + math.rad(tonumber(opt.boxsunoff) or 35)
    if math.abs(sx) + math.abs(sz) < 1e-3 then a = 0 end
    fx, fz = math.sin(a), math.cos(a)
    sunKnown = true
  end
end

local function FlattestSpot()
  if opt.boxx and opt.boxz then return tonumber(opt.boxx), tonumber(opt.boxz) end
  local minH, maxH = Spring.GetGroundExtremes()
  local floor = minH + (maxH - minH) * 0.25
  local best, bx, bz
  for x = 900, Game.mapSizeX - 900, 128 do
    for z = 1400, Game.mapSizeZ - 500, 128 do
      local h0 = Spring.GetGroundHeight(x, z)
      if h0 > math.max(5, floor) then
        local sum, sum2, n = 0, 0, 0
        for dx = -700, 700, 100 do
          for dz = -1200, 500, 100 do
            local h = Spring.GetGroundHeight(x + dx, z + dz)
            sum, sum2, n = sum + h, sum2 + h * h, n + 1
            if h < 1 then sum2 = sum2 + 1e6 end   -- water or lava
          end
        end
        local var = sum2 / n - (sum / n) ^ 2
        if not best or var < best then best, bx, bz = var, x, z end
      end
    end
  end
  Spring.Echo(string.format("[BOXART] spot %d,%d height variance %.0f", bx or -1, bz or -1, best or -1))
  return bx or Game.mapSizeX / 2, bz or Game.mapSizeZ / 2
end

local function Place(name, lx, lz)
  local ud = UnitDefNames[name]
  if not ud then Spring.Echo("[BOXART] no unit " .. name) return end
  local x, z = W(lx, lz)
  return Spring.CreateUnit(name, x, Spring.GetGroundHeight(x, z), z, Facing(), 0)
end

function gadget:GameStart()
  -- an enemy commander far away, so the game does not offer a surrender vote
  Spring.CreateUnit(SIDE == "arm" and "core_commander" or "arm_commander", 200, Spring.GetGroundHeight(200, 200), 200, "south", 1)
end

function gadget:Initialize()
  for id = 1, #WeaponDefs do Script.SetWatchProjectile(id, true) end
end

local shotFrame
function gadget:ProjectileCreated(proID, ownerID, weaponDefID)
  local wd = WeaponDefs[weaponDefID]
  if ownerID and ownerID == com and not shotFrame and wd and (wd.manualFire or wd.commandfire) then
    shotFrame = Spring.GetGameFrame()
    Spring.Echo("[BOXART] D-Gun shot " .. wd.name .. " frame " .. shotFrame)
  end
end

function gadget:GameFrame(n)
  if shotFrame and not Spring.GetGameRulesParam("boxart_shot") then
    Spring.SetGameRulesParam("boxart_shot", shotFrame)
  end
  if not setupDone and n >= 2 and (sunKnown or n >= 30) then
    setupDone = true
    Spring.SendCommands("cheat 1", "godmode 1", "globallos")
    for _, t in ipairs(Spring.GetTeamList()) do
      Spring.SetTeamResource(t, "es", 1e7) Spring.SetTeamResource(t, "e", 1e7)
      Spring.SetTeamResource(t, "ms", 1e7) Spring.SetTeamResource(t, "m", 1e7)
    end
    cx, cz = FlattestSpot()
    local base = BASES[SIDE]
    for _, b in ipairs(base.buildings) do Place(b[1], b[2], b[3]) end
    for _, u in ipairs(base.units) do Place(u[1], u[2], u[3]) end
    for _, u in ipairs(base.air) do
      local id = Place(u[1], u[2], u[3])
      local x, z = W(u[2], u[3])
      if id then Spring.GiveOrderToUnit(id, CMD.MOVE, { x, 0, z }, 0) end
    end
    com = Place(SIDE .. "_commander", 0, 0)
    Spring.SetGameRulesParam("boxart_x", cx)
    Spring.SetGameRulesParam("boxart_z", cz)
    Spring.SetGameRulesParam("boxart_fx", fx)
    Spring.SetGameRulesParam("boxart_fz", fz)
    Spring.Echo(string.format("[BOXART] front %.2f,%.2f (%s)", fx, fz, Facing()))
    Spring.SetGameRulesParam("boxart_com", com)
  end
  -- the base's guns fire at the far distance behind it
  if n >= 60 and n % 45 == 0 and cx then
    for _, id in ipairs(Spring.GetTeamUnits(0)) do
      local ud = UnitDefs[Spring.GetUnitDefID(id)]
      local wd = ud.weapons[1] and WeaponDefs[ud.weapons[1].weaponDef]
      if id ~= com and wd and wd.range < 900 and not ud.canFly then   -- no artillery: its trails streak the sky
        local x, _, z = Spring.GetUnitPosition(id)
        local back, lat = math.random(250, 500), math.random(-300, 300)
        local tx, tz = x + lat * fz - fx * back, z - lat * fx - fz * back
        Spring.GiveOrderToUnit(id, CMD.ATTACK, { tx, Spring.GetGroundHeight(tx, tz), tz }, 0)
      end
    end
  end
  -- boxbuild=<unit>: the commander builds it instead (a nanoframe boxprogress built, at boxbangle degrees from
  -- straight ahead, just inside its build range); the pause comes boxpause frames after the order
  if opt.boxbuild and n == FIRE_FRAME and com then
    local ud = UnitDefNames[opt.boxbuild]
    if not ud then Spring.Echo("[BOXART] no unit " .. tostring(opt.boxbuild)) return end
    local cd = UnitDefs[Spring.GetUnitDefID(com)]
    local dist = (cd.buildDistance or 100) * 0.5 + ud.radius * 0.8
    local a = math.rad(tonumber(opt.boxbangle) or -45)
    local bx, bz = W(math.sin(a) * dist, math.cos(a) * dist)
    local frame = Spring.CreateUnit(opt.boxbuild, bx, Spring.GetGroundHeight(bx, bz), bz, Facing(), 0, true)
    if frame then
      Spring.SetUnitHealth(frame, { build = tonumber(opt.boxprogress) or 0.5, health = ud.health * 0.5 })
      Spring.GiveOrderToUnit(com, CMD.REPAIR, { frame }, 0)
    end
    Spring.Echo(string.format("[BOXART] building %s at %d,%d (%d elmos), build distance %d", opt.boxbuild, bx, bz, dist, cd.buildDistance or -1))
    shotFrame = n
    return
  end
  if n == FIRE_FRAME and com then
    -- the D-Gun goes off toward the front left, past the camera
    -- inside the D-Gun's range, or the commander walks off toward the target
    local range = 200
    for _, w in ipairs(UnitDefs[Spring.GetUnitDefID(com)].weapons) do
      local wd = WeaponDefs[w.weaponDef]
      if wd.manualFire or wd.commandfire then range = wd.range end
    end
    local ahead = range * 0.85
    local tx, tz = W((tonumber(opt.boxaimx) or -0.2) * ahead, ahead)
    -- boxaimcam=<preset>: toward that camera, turned boxaimdeg degrees aside (the gun points at the viewer)
    for _, cam in ipairs(CAMS) do
      if cam.name == opt.boxaimcam then
        local a = math.atan2(cam.side, cam.dist) + math.rad(tonumber(opt.boxaimdeg) or 12)
        tx, tz = W(math.sin(a) * ahead, math.cos(a) * ahead)
      end
    end
    Spring.Echo(string.format("[BOXART] D-Gun range %d, aim %d,%d", range, tx, tz))
    Spring.GiveOrderToUnit(com, CMD.MANUALFIRE, { tx, Spring.GetGroundHeight(tx, tz), tz }, 0)
    Spring.SetGameRulesParam("boxart_fired", n)
  end
end

else -- UNSYNCED: pause, camera, screenshots

local state, idx, waitUntil = "wait", 0, 0
local logged, sunSent, lit

-- boxlight=<preset>: the scene's light, set like a photo shoot (the Weather widget is off). The sun's direction is
-- relative to the scene: az 0 = from behind the camera, 90 = from the right; el = height in degrees.
local LIGHTS = {
  arm = { az = 40, el = 22, key = {1.25, 1.05, 0.85}, amb = {0.24, 0.30, 0.46}, spec = {0.9, 0.9, 1.0},
          fog = {0.42, 0.52, 0.72}, fogStart = 0.6, sky = {0.32, 0.42, 0.66}, sunColor = {1.0, 0.85, 0.6} },
  core = { az = -50, el = 15, key = {1.45, 0.62, 0.30}, amb = {0.24, 0.09, 0.08}, spec = {1.0, 0.6, 0.4},
           fog = {0.32, 0.08, 0.04}, fogStart = 0.6, sky = {0.25, 0.06, 0.03}, sunColor = {1.0, 0.45, 0.2} },
}
local function ApplyLight()
  local L = LIGHTS[opt.boxlight or ""]
  if not L then return end
  local fx, fz = Spring.GetGameRulesParam("boxart_fx") or 0, Spring.GetGameRulesParam("boxart_fz") or 1
  local az, el = math.rad(L.az), math.rad(L.el)
  local lx, lz = math.sin(az) * math.cos(el), math.cos(az) * math.cos(el)
  Spring.SetSunDirection(lx * fz + lz * fx, math.sin(el), -lx * fx + lz * fz)
  Spring.SetSunLighting({
    groundAmbientColor = L.amb, groundDiffuseColor = L.key, groundSpecularColor = L.spec,
    unitAmbientColor = L.amb, unitDiffuseColor = L.key, unitSpecularColor = L.spec,
  })
  -- haze only: the map's own sky (skybox, clouds, stars) stays
  Spring.SetAtmosphere({ fogStart = L.fogStart, fogEnd = 1.0, fogColor = {L.fog[1], L.fog[2], L.fog[3], 1},
    sunColor = L.sunColor })
  Spring.Echo("[BOXART] light " .. opt.boxlight)
end

local function SetCam(cam)
  local cx, cz = Spring.GetGameRulesParam("boxart_x"), Spring.GetGameRulesParam("boxart_z")
  local com = Spring.GetGameRulesParam("boxart_com")
  local ux, uy, uz = Spring.GetUnitPosition(com)
  ux, uy, uz = ux or cx, uy or Spring.GetGroundHeight(cx, cz), uz or cz
  local fx, fz = Spring.GetGameRulesParam("boxart_fx") or 0, Spring.GetGameRulesParam("boxart_fz") or 1
  local px, pz = ux + cam.side * fz + cam.dist * fx, uz - cam.side * fx + cam.dist * fz
  local py = math.max(uy + cam.height, Spring.GetGroundHeight(px, pz) + 5)
  local lx, ly, lz = ux, uy + cam.look, uz
  local dx, dy, dz = lx - px, ly - py, lz - pz
  local len = math.sqrt(dx * dx + dy * dy + dz * dz)
  dx, dy, dz = dx / len, dy / len, dz / len
  local st = Spring.GetCameraState()
  st.px, st.py, st.pz = px, py, pz
  st.dx, st.dy, st.dz = dx, dy, dz
  -- FPS camera rotation (engine CCamera::GetFwdFromRot: fwd = (sin rx sin ry, cos rx, -sin rx cos ry))
  st.rx = math.acos(dy)
  st.ry = math.atan2(dx, -dz)
  st.rz = 0
  st.fov = tonumber(opt.boxfov) or 40
  st.oldHeight = py
  Spring.SetCameraState(st, 0)
end

function gadget:Update()
  local fired = Spring.GetGameRulesParam("boxart_shot")
  if not sunSent then
    sunSent = true
    local sx, sy, sz = gl.GetSun("pos")
    Spring.SendLuaRulesMsg(string.format("boxart_sun:%.4f:%.4f", sx or 0, sz or 1))
  end
  if state == "wait" then
    if Spring.GetGameRulesParam("boxart_com") and not logged then
      logged = true
      -- keep LuaUI for the graphics widgets (bloom, SSAO, lights...), hide the interface
      Spring.SendCommands("luaui disablewidget Initial Settings", "hideinterface 1", "console 0", "viewfps", "disticon 100000",
        "luaui enablewidget SSAO", "luaui enablewidget Map Grass GL4", "luaui disablewidget GFX Rain",
        "luaui disablewidget Snow", "luaui disablewidget Health Bars GL4", "luaui disablewidget Range Overview GL4",
        "luaui disablewidget Altitude Lines GL4", "luaui disablewidget Aircraft Trails GL4", "luaui disablewidget Weather")
      for w in tostring(opt.boxoff or ""):gmatch("[^,]+") do Spring.SendCommands("luaui disablewidget " .. w) end
      Spring.Echo(string.format("[BOXART] team 0 colour %.2f %.2f %.2f", Spring.GetTeamColor(0)))
    end
    if logged and not lit and Spring.GetGameRulesParam("boxart_fx") and Spring.GetGameFrame() > 20 then
      lit = true
      ApplyLight()
    end
    if fired and Spring.GetGameFrame() >= fired + PAUSE_AFTER then
      Spring.SendCommands("pause 1")
      state, idx, waitUntil = "shoot", 0, os.clock() + 1.5
    end
  elseif state == "shoot" and os.clock() >= waitUntil then
    if idx > 0 then
      Spring.SendCommands("screenshot png")
      Spring.Echo("[BOXART] shot " .. CAMS[idx].name .. " frame " .. Spring.GetGameFrame())
    end
    idx = idx + 1
    if idx > #CAMS then
      state, waitUntil = "quit", os.clock() + 2
      return
    end
    SetCam(CAMS[idx])
    local st = Spring.GetCameraState()
    local parts = {}
    for k, v in pairs(st) do parts[#parts + 1] = k .. "=" .. tostring(type(v) == "number" and math.floor(v * 1000) / 1000 or v) end
    table.sort(parts)
    Spring.Echo("[BOXART] cam " .. CAMS[idx].name .. ": " .. table.concat(parts, " "))
    waitUntil = os.clock() + 1.2
  elseif state == "quit" and os.clock() >= waitUntil then
    Spring.SendCommands("quitforce")
    state = "done"
  end
end

end
