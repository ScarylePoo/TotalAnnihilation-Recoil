function widget:GetInfo() return { name = "Lights Leak Probe", layer = 99997, enabled = true } end
-- LIGHTSPROBE=1 run_win_visual.sh (with VISUALSELECT=1 so LuaUI stays on): every 60 frames counts the entries of
-- the deferred lights widget's unit-bound light buffers whose unit no longer exists (lights of dead units that
-- nobody removed; they corrupt the buffer on its next resize) and the units the unit tracker still lists that are
-- gone. Both must stay at 0.
if not (Spring.GetModOptions() or {}).lightsprobe then return false end

local function leaked(vbo)
  if not vbo or not vbo.indextoUnitID then return "-", "-" end
  local bad = 0
  for i = 1, vbo.usedElements do
    local u = vbo.indextoUnitID[i]
    if u and not Spring.ValidUnitID(u) then bad = bad + 1 end
  end
  return vbo.usedElements, bad
end

function widget:GameFrame(f)
  if f % 60 ~= 0 or f == 0 then return end
  local api = WG.lightsgl4
  local pu, pl = leaked(api and api.GetLightVBO and api.GetLightVBO("unitPointLightVBO"))
  local cu, cl = leaked(api and api.GetLightVBO and api.GetLightVBO("unitConeLightVBO"))
  local tracked, stale = 0, 0
  if WG.unittrackerapi and WG.unittrackerapi.visibleUnits then
    for u in pairs(WG.unittrackerapi.visibleUnits) do
      tracked = tracked + 1
      if not Spring.ValidUnitID(u) or Spring.GetUnitIsDead(u) ~= false then stale = stale + 1 end
    end
  end
  Spring.Echo(("[LIGHTSPROBE] f=%d point used=%s leaked=%s | cone used=%s leaked=%s | tracker units=%d stale=%d | units alive=%d")
    :format(f, tostring(pu), tostring(pl), tostring(cu), tostring(cl), tracked, stale, #Spring.GetAllUnits()))
end
