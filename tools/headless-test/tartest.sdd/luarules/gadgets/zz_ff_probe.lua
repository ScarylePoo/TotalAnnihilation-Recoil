function gadget:GetInfo()
  return { name = "Friendly Fire Probe", layer = 1005, enabled = true }
end

-- FFPROBE=1 run.sh: ordinary friendly fire does nothing, enemy damage lands, and the TA exceptions still hurt your own
-- units: a team-0 LLT "shoots" (AddUnitDamage, its laser) a team-0 and a team-1 Bulldog; then a team-0 D-Gun hit on
-- both; then a team-0 fusion plant between them self-destructs.
-- Logs "[PROBE] ff <unit> health a/b" after each step.
if not gadgetHandler:IsSyncedCode() or not (Spring.GetModOptions() or {}).ffprobe then return end

local cx, cz = Game.mapSizeX / 2, Game.mapSizeZ / 2
local u = {}

local function Report(step)
  for _, k in ipairs({ "own", "enemy" }) do
    local h, mh = Spring.GetUnitHealth(u[k])
    Spring.Echo(string.format("[PROBE] ff %s %s health %s/%s", step, k, tostring(h and math.floor(h)), tostring(mh and math.floor(mh))))
  end
end

function gadget:GameFrame(n)
  if n == 30 then
    Spring.SendCommands("cheat 1", "godmode 0")
    local y = Spring.GetGroundHeight(cx, cz)
    u.shooter = Spring.CreateUnit("arm_t1_def_llt", cx, y, cz - 300, "south", 0)
    u.own     = Spring.CreateUnit("arm_t2_veh_bulldog", cx - 60, y, cz, "south", 0)
    u.enemy   = Spring.CreateUnit("arm_t2_veh_bulldog", cx + 60, y, cz, "south", 1)
    u.fusion  = Spring.CreateUnit("arm_t2_eco_fusionpowerplant", cx, y, cz + 80, "south", 0)
    Report("start")
  elseif n == 40 then
    local laser = WeaponDefNames["arm_tower_light_laser"].id
    Spring.AddUnitDamage(u.own, 500, 0, u.shooter, laser)
    Spring.AddUnitDamage(u.enemy, 500, 0, u.shooter, laser)
  elseif n == 45 then
    Report("after-500-laser")
    local dgun = WeaponDefNames["disintegrator"].id
    Spring.AddUnitDamage(u.own, 300, 0, u.shooter, dgun)
    Spring.AddUnitDamage(u.enemy, 300, 0, u.shooter, dgun)
  elseif n == 50 then
    Report("after-300-dgun")
    Spring.DestroyUnit(u.fusion, true)
  elseif n == 120 then
    Report("after-fusion-blast")
  elseif n == 130 then
    Spring.Echo("[PROBE] ff done")
  end
end
