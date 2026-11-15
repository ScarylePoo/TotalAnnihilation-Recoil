function gadget:GetInfo()
  return { name = "Last Seen Probe", layer = 1008, enabled = true }
end

-- AIRPROBE=lost tools/headless-test/run.sh <engine>: luarules/gadgets/unit_air_lastseen.lua. Each plane attacks an enemy
-- vehicle 3000 elmos away that is always visible; 5 s in, the vehicle loses that and is out of LOS and radar:
--   moved   it is teleported 3000 elmos further on: the plane should run on the OLD spot, hit nothing, then finish
--   stays   it stays put: the plane should switch back to the vehicle when it sees it again, and hit it
--   radar   an allied radar tower covers it: the order stays on the vehicle; 10 s later the tower dies and the
--           plane runs on the radar dot (logged: distance of the ground order from the vehicle = the radar error)
-- [PROBE] lost <unit> <case> shots hits cmds=<head command over time: unit@t ground(d=<dist to vehicle>)@t done@t>
local opt = Spring.GetModOptions() or {}
if opt.airprobe ~= "lost" or not gadgetHandler:IsSyncedCode() then return end

local PLANES = { "arm_t1_air_thunder", "core_t1_air_shadow", "arm_t2_air_phoenix", "arm_t2_air_brawler", "arm_t1_air_freedomfighter" }
local TARGET = "core_t1_veh_weasel"
local cases = {}
local END = 30 + 75 * 30

local function Head(c)
  if not Spring.ValidUnitID(c.u) then return "dead" end
  local id, _, _, a1, a2, a3 = Spring.GetUnitCurrentCommand(c.u)
  if id ~= CMD.ATTACK then return "done" end
  if a2 == nil then return a1 == c.t and "unit" or "other" end
  local x, _, z = Spring.GetUnitPosition(c.t)
  local ox, oz = c.ox, c.oz
  return string.format("ground(d=%.0f,dOld=%.0f)", math.sqrt((a1 - x) ^ 2 + (a3 - z) ^ 2), math.sqrt((a1 - ox) ^ 2 + (a3 - oz) ^ 2))
end

function gadget:GameFrame(n)
  if n == 20 then
    Spring.SendCommands("cheat 1", "setmaxspeed 100", "setminspeed 100")
    local X = 400
    local Z = Game.mapSizeZ - 400
    for _, name in ipairs(PLANES) do
      for _, kind in ipairs({ "moved", "stays", "radar" }) do
        local u = Spring.CreateUnit(name, X, Spring.GetGroundHeight(X, Z), Z, "north", 0)
        local tz = Z - 3000
        local t = Spring.CreateUnit(TARGET, X, Spring.GetGroundHeight(X, tz), tz, "north", 1)
        Spring.SetUnitMaxHealth(t, 1e7); Spring.SetUnitHealth(t, 1e7)
        Spring.SetUnitAlwaysVisible(t, true)
        Spring.GiveOrderToUnit(t, CMD.FIRE_STATE, { 0 }, 0)
        local r
        if kind == "radar" then
          -- a tower next to the vehicle with its radar cut to 300 and no sight, so it covers only this vehicle
          r = Spring.CreateUnit("arm_t1_def_radartower", X + 120, Spring.GetGroundHeight(X + 120, tz), tz, "north", 0)
          Spring.SetUnitSensorRadius(r, "radar", 300)
          Spring.SetUnitSensorRadius(r, "los", 0)
          Spring.SetUnitSensorRadius(r, "airLos", 0)
        end
        for w = 1, #UnitDefs[Spring.GetUnitDefID(u)].weapons do
          Script.SetWatchWeapon(UnitDefs[Spring.GetUnitDefID(u)].weapons[w].weaponDef, true)
        end
        cases[#cases + 1] = { u = u, t = t, r = r, kind = kind, name = name, shots = 0, hits = 0, log = {}, ox = X, oz = tz }
        X = X + 600
      end
    end
  end
  if n == 30 then
    for _, c in ipairs(cases) do Spring.GiveOrderToUnit(c.u, CMD.ATTACK, { c.t }, 0) end
  end
  if n == 30 + 150 then
    for _, c in ipairs(cases) do
      Spring.SetUnitAlwaysVisible(c.t, false)
      if c.kind == "moved" then
        Spring.SetUnitPosition(c.t, c.ox, c.oz - 3000)   -- well past where any plane flies
      end
    end
  end
  if n == 30 + 450 then
    for _, c in ipairs(cases) do if c.r and Spring.ValidUnitID(c.r) then Spring.DestroyUnit(c.r, false, true) end end
  end
  if n > 30 and n % 15 == 0 and n <= END then
    for _, c in ipairs(cases) do
      local h = Head(c)
      local key = h:match("^%a+")
      if key ~= c.lastKey then
        c.log[#c.log + 1] = string.format("%s@%.1f", h, (n - 30) / 30)
        c.lastKey = key
      end
    end
  end
  if n == END + 10 then
    for _, c in ipairs(cases) do
      local los = Spring.GetUnitLosState(c.t, 0)
      Spring.Echo(string.format("[PROBE] lost %s %s shots=%d hits=%d los=%s radar=%s cmds=%s", c.name, c.kind, c.shots, c.hits,
        tostring(los and los.los), tostring(los and los.radar), table.concat(c.log, " ")))
    end
    Spring.SendCommands("quitforce")
  end
end

function gadget:ProjectileCreated(proID, ownerID)
  for _, c in ipairs(cases) do if c.u == ownerID then c.shots = c.shots + 1 end end
end

function gadget:UnitDamaged(unitID, unitDefID, unitTeam, damage, paralyzer, weaponDefID, projectileID, attackerID)
  for _, c in ipairs(cases) do if c.t == unitID and attackerID == c.u then c.hits = c.hits + 1 end end
end
