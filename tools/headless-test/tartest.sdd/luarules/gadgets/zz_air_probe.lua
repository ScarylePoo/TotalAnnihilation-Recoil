function gadget:GetInfo()
  return { name = "Air Probe", layer = 1007, enabled = true }
end

-- AIRPROBE=1 tools/headless-test/run.sh <engine>: how the aircraft fly and fight. Every plane starts on the ground.
--   hop    every aircraft is ordered to a point 250 elmos ahead: does it get there, or take off and land on the spot?
--          [PROBE] hop <unit> reached=<dist to goal at the end> maxalt=<highest above ground> state=<flying/landed...>
--   bomb   every bomber/torpedo bomber/gunship/fighter with a ground weapon attacks an enemy building 3000 elmos away
--          (attack unit) and a second copy attacks the ground next to one (attack ground), 60 s each:
--          [PROBE] attack <unit> <unit|ground> shots=<n> hits=<n on the target> dmg=<total> first=<s to first shot>
--          firsthit=<s> passes=<times it flew over the target> cmd=<order still queued at the end?>
--   air    every fighter attacks an enemy Thunder flying a patrol (dps on air targets).
-- AIRPROBE=unit1,unit2 limits the units.
local opt = Spring.GetModOptions() or {}
if not opt.airprobe or not gadgetHandler:IsSyncedCode() then return end

local want
if opt.airprobe ~= "1" then
  want = {}
  for n in opt.airprobe:gmatch("[^,]+") do want[n:lower()] = true end
end

local GROUND_TARGET = "core_t1_eco_metalstorage"
local hops, attacks, airs = {}, {}, {}
local byProj = {}     -- projectileID -> attack record
local DURATION = 1800

local function aircraftState(u)
  local d = Spring.GetUnitMoveTypeData(u)
  return d and d.aircraftState or "?"
end

local function GroundWeapon(ud)
  for _, w in ipairs(ud.weapons) do
    local wd = WeaponDefs[w.weaponDef]
    if wd and not (w.onlyTargets and w.onlyTargets.vtol and not w.onlyTargets.notair) and wd.damages[0] > 1 then
      return wd
    end
  end
end

local function Spawn(name, x, z, team, facing)
  local u = Spring.CreateUnit(name, x, Spring.GetGroundHeight(x, z), z, facing or "north", team)
  return u
end

function gadget:GameFrame(n)
  if n == 20 then
    Spring.SendCommands("cheat 1", "setmaxspeed 100", "setminspeed 100")
    Spring.SetGlobalLos(0, true)   -- attack orders on units out of sight get dropped
    local X = 300
    local Z = Game.mapSizeZ - 400
    for id, ud in pairs(UnitDefs) do
      if ud.canFly and (not want or want[ud.name]) and not ud.name:find("decoy") then
        -- hop
        local u = Spawn(ud.name, X, Z, 0)
        if u then hops[#hops + 1] = { u = u, name = ud.name, goal = { X, 0, Z - 250 }, maxalt = 0 } end
        -- attacks
        local wd = GroundWeapon(ud)
        local torp = ud.weapons[1] and WeaponDefs[ud.weapons[1].weaponDef]
        if torp and torp.type == "TorpedoLauncher" then
          -- torpedo bombers: attack an enemy ship in a lake 3000 elmos away
          local tz = Z - 900 - 3000
          Spring.SetHeightMapFunc(function()
            for x = X - 120, X + 120, 8 do for z = tz - 1400, tz + 600, 8 do Spring.SetHeightMap(x, z, -120) end end
          end)
          local a = Spawn(ud.name, X, Z - 900, 0)
          local t = Spawn("core_t1_sea_searcher", X, tz, 1)
          if ud.name:find("^core") then t = Spawn("arm_t1_sea_skeeter", X, tz, 1) end
          if a and t then
            Spring.SetUnitMaxHealth(t, 1e7); Spring.SetUnitHealth(t, 1e7)
            Script.SetWatchWeapon(torp.id, true)
            attacks[#attacks + 1] = { u = a, t = t, kind = "ship", name = ud.name, wd = torp, shots = 0, hits = 0,
              dmg = 0, passes = 0, tx = X, tz = tz, near = false }
          end
          wd = nil
        end
        if wd then
          for _, kind in ipairs({ "unit", "ground" }) do
            local ax = X + (kind == "ground" and 90 or 0)
            local a = Spawn(ud.name, ax, Z - 900, 0)
            local tz = Z - 900 - 3000
            local t = Spawn(GROUND_TARGET, ax, tz, 1)
            if a and t then
              Spring.SetUnitMaxHealth(t, 1e7); Spring.SetUnitHealth(t, 1e7)
              Script.SetWatchWeapon(wd.id, true)
              attacks[#attacks + 1] = { u = a, t = t, kind = kind, name = ud.name, wd = wd, shots = 0, hits = 0,
                dmg = 0, passes = 0, tx = ax, tz = tz, near = false }
            end
          end
        end
        -- air: every unit whose weapon only targets aircraft attacks an enemy Shadow circling 2500 elmos ahead
        local aw = ud.weapons[1] and WeaponDefs[ud.weapons[1].weaponDef]
        if aw and (aw.type == "AircraftBomb" or aw.type == "TorpedoLauncher") then aw = nil end
        if aw then
          local f = Spawn(ud.name, X + 45, Z - 1800, 0)
          local tz = Z - 1800 - 2500
          local t = Spawn("core_t1_air_shadow", X + 45, tz, 1)
          if f and t then
            Spring.SetUnitMaxHealth(t, 1e7); Spring.SetUnitHealth(t, 1e7)
            Script.SetWatchWeapon(aw.id, true)
            attacks[#attacks + 1] = { u = f, t = t, kind = "air", name = ud.name, wd = aw, shots = 0, hits = 0,
              dmg = 0, passes = 0, tx = X + 45, tz = tz, near = false, patrol = true }
          end
        end
        X = X + 260
      end
    end
  end
  if n == 30 then
    for _, h in ipairs(hops) do Spring.GiveOrderToUnit(h.u, CMD.MOVE, h.goal, 0) end
    for _, a in ipairs(attacks) do
      if a.patrol then
        Spring.GiveOrderToUnit(a.t, CMD.PATROL, { a.tx + 1200, 0, a.tz }, 0)
        Spring.GiveOrderToUnit(a.u, CMD.ATTACK, { a.t }, 0)
      elseif a.kind == "unit" then
        Spring.GiveOrderToUnit(a.u, CMD.ATTACK, { a.t }, 0)
      else
        Spring.GiveOrderToUnit(a.u, CMD.ATTACK, { a.tx + 40, Spring.GetGroundHeight(a.tx + 40, a.tz), a.tz }, 0)
      end
    end
  end
  if n > 30 and n <= 30 + DURATION then
    for _, h in ipairs(hops) do
      if Spring.ValidUnitID(h.u) then
        local x, y, z = Spring.GetUnitPosition(h.u)
        h.maxalt = math.max(h.maxalt, y - Spring.GetGroundHeight(x, z))
        if n == 30 + 450 then
          h.dist = math.sqrt((x - h.goal[1]) ^ 2 + (z - h.goal[3]) ^ 2)
          h.state = aircraftState(h.u)
          h.alt = y - Spring.GetGroundHeight(x, z)
        end
      end
    end
    for _, a in ipairs(attacks) do
      if Spring.ValidUnitID(a.u) then
        local x, _, z = Spring.GetUnitPosition(a.u)
        local near = (x - a.tx) ^ 2 + (z - a.tz) ^ 2 < 250 ^ 2
        if near and not a.near then a.passes = a.passes + 1 end
        a.near = near
      end
    end
  end
  if n == 30 + DURATION + 60 then
    for _, h in ipairs(hops) do
      local x, y, z = Spring.GetUnitPosition(h.u)
      local dEnd = x and math.sqrt((x - h.goal[1]) ^ 2 + (z - h.goal[3]) ^ 2)
      Spring.Echo(string.format("[PROBE] hop %s dist=%s alt@15s=%s maxalt=%.0f state=%s | @60s dist=%s state=%s", h.name,
        h.dist and string.format("%.0f", h.dist) or "-", h.alt and string.format("%.0f", h.alt) or "-", h.maxalt, tostring(h.state),
        dEnd and string.format("%.0f", dEnd) or "-", x and tostring(aircraftState(h.u)) or "-"))
    end
    for _, a in ipairs(attacks) do
      local q = Spring.ValidUnitID(a.u) and Spring.GetUnitCommands(a.u, 1) or {}
      if a.kind == "ship" then
        local hp = Spring.ValidUnitID(a.t) and Spring.GetUnitHealth(a.t)
        local x, y, z = Spring.GetUnitPosition(a.t)
        Spring.Echo(string.format("[PROBE] ship target %s hp=%s y=%s", a.name, tostring(hp), tostring(y)))
      end
      Spring.Echo(string.format("[PROBE] attack %s %s wpn=%s shots=%d hits=%d dmg=%.0f first=%s firsthit=%s passes=%d cmd=%s",
        a.name, a.kind, a.wd.name, a.shots, a.hits, a.dmg, a.first and string.format("%.1f", a.first / 30) or "-",
        a.firsthit and string.format("%.1f", a.firsthit / 30) or "-", a.passes, (q[1] and q[1].id == CMD.ATTACK) and "attack" or "done"))
    end
    Spring.SendCommands("quitforce")
  end
end

local function RecordFor(ownerID)
  for _, a in ipairs(attacks) do
    if a.u == ownerID then return a end
  end
end

function gadget:ProjectileCreated(proID, ownerID, weaponDefID)
  local a = ownerID and RecordFor(ownerID)
  if a and weaponDefID == a.wd.id then
    a.shots = a.shots + 1
    a.first = a.first or (Spring.GetGameFrame() - 30)
  end
end

function gadget:UnitDamaged(unitID, unitDefID, unitTeam, damage, paralyzer, weaponDefID, projectileID, attackerID)
  for _, a in ipairs(attacks) do
    if a.t == unitID and (attackerID == a.u) then
      a.hits = a.hits + 1
      a.dmg = a.dmg + damage
      a.firsthit = a.firsthit or (Spring.GetGameFrame() - 30)
    end
  end
end
