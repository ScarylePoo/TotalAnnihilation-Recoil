function gadget:GetInfo()
  return { name = "Flight Probe", layer = 1006, enabled = true }
end

-- FLIGHT=1 tools/headless-test/run.sh <frames>: every aircraft (or FLIGHT=unit1,unit2) starts on the ground and is
-- ordered across the map at frame 30; logs per unit when it reaches 50 % / 90 % of its top speed and its peak speed.
--   FLIGHTP <name> max=<elmos/frame> t50=<frames> t90=<frames> peak=<elmos/frame>
local opt = Spring.GetModOptions() or {}
if not opt.flightprobe or not gadgetHandler:IsSyncedCode() then return end

local units = {}

function gadget:GameStart()
  local want = {}
  if opt.flightprobe ~= "1" then
    for n in opt.flightprobe:gmatch("[^,]+") do want[n:lower()] = true end
  end
  local x = 300
  for id, ud in pairs(UnitDefs) do
    if ud.canFly and (opt.flightprobe == "1" or want[ud.name]) and not ud.name:find("decoy") then
      local u = Spring.CreateUnit(id, x, Spring.GetGroundHeight(x, Game.mapSizeZ - 400), Game.mapSizeZ - 400, "north", 0)
      if u then units[u] = { name = ud.name, max = ud.speed / 30, peak = 0 } end
      x = x + 180
    end
  end
  Spring.CreateUnit("core_commander", Game.mapSizeX - 200, 0, 200, "south", 1)
end

function gadget:GameFrame(n)
  for u, d in pairs(units) do
    if n == 30 then
      local x, _, z = Spring.GetUnitPosition(u)
      Spring.GiveOrderToUnit(u, CMD.MOVE, { x, 0, 200 }, {})
    elseif n > 30 and Spring.ValidUnitID(u) then
      local _, _, _, w = Spring.GetUnitVelocity(u)
      w = w or 0
      d.peak = math.max(d.peak, w)
      if not d.t50 and w >= 0.5 * d.max then d.t50 = n - 30 end
      if not d.t90 and w >= 0.9 * d.max then d.t90 = n - 30 end
    end
  end
  if n == 30 + 900 then
    for _, d in pairs(units) do
      Spring.Echo(string.format("FLIGHTP %s max=%.2f t50=%s t90=%s peak=%.2f", d.name, d.max, tostring(d.t50), tostring(d.t90), d.peak))
    end
  end
end
