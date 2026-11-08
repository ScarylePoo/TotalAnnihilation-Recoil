function gadget:GetInfo()
  return { name = "Turn Probe", layer = 1005, enabled = true }
end

-- TURNPROBE=1 run.sh: a Flash running east at full speed is ordered to a point 60 and then (another one) 150 degrees
-- off its heading; logs "[PROBE] turn" with its lowest speed over the next 2 s, as a share of top speed.
if not gadgetHandler:IsSyncedCode() or not (Spring.GetModOptions() or {}).turnprobe then return end

local runs = {}
local function Start(angle, z)
  local id = Spring.CreateUnit("arm_t1_veh_flash", 600, Spring.GetGroundHeight(600, z), z, "east", 0)
  Spring.GiveOrderToUnit(id, CMD.MOVE, { 5000, 0, z }, 0)
  runs[#runs + 1] = { id = id, angle = angle, z = z }
end

function gadget:GameFrame(n)
  if n == 30 then
    Spring.SendCommands("cheat 1", "godmode 1")
    Start(60, 1500)
    Start(150, 3000)
  end
  for _, r in ipairs(runs) do
    if n == 150 then
      local x, _, z = Spring.GetUnitPosition(r.id)
      local a = math.rad(r.angle)
      r.top = select(4, Spring.GetUnitVelocity(r.id))
      Spring.GiveOrderToUnit(r.id, CMD.MOVE, { x + math.cos(a) * 700, 0, z - math.sin(a) * 700 }, 0)
      r.min = r.top
    elseif n > 150 and n <= 210 then
      r.min = math.min(r.min, select(4, Spring.GetUnitVelocity(r.id)))
    elseif n == 211 then
      Spring.Echo(string.format("[PROBE] turn %d deg: speed before %.2f, lowest %.2f (%.0f%%) (moveturninplace %s)",
        r.angle, r.top, r.min, 100 * r.min / r.top, tostring((Spring.GetModOptions() or {}).moveturninplace or "default")))
    end
  end
  if n == 230 then Spring.SendCommands("quitforce") end
end
