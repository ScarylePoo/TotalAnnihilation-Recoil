function widget:GetInfo()
  return { name = "Geo Probe", layer = 100000, enabled = true, handler = true }  -- handler: the real widgetHandler, for its widget list
end
-- see luarules/gadgets/zz_geo_probe.lua
local opt = Spring.GetModOptions() or {}
if not (opt.geoprobe and opt.geoprobe ~= "") then return end

local vx, vz
-- the order goes through the network: in this harness the sim runs far ahead of the draw loop, so it lands
-- some 30 frames after the click
local HOVER_FROM, CLICK_AT, CHECK_AT = 90, 230, 300
local clicked = false

local function log(ok, what, ...) Spring.Echo("[GEOPROBE]", ok and "PASS" or "FAIL", what, ...) end

function widget:Update()
  local n = Spring.GetGameFrame()
  if n < HOVER_FROM then return end
  vx = vx or Spring.GetGameRulesParam("geoprobe_x")
  vz = vz or Spring.GetGameRulesParam("geoprobe_z")
  if not vx then return end
  -- look straight down on the vent, mouse at the screen's centre: that is the vent
  local vy = Spring.GetGroundHeight(vx, vz)
  Spring.SetCameraState({ name = "spring", mode = 2, px = vx, py = vy, pz = vz, dist = 700, rx = 2.6, ry = math.pi, rz = 0, fov = 45 }, 0)
  -- the mouse on the vent wherever the camera ends up (the visual probe gadget moves it too)
  local sx, sy = Spring.WorldToScreenCoords(vx, vy, vz)
  if sx then Spring.WarpMouse(math.floor(sx), math.floor(sy)) end
end

function widget:GameFrame(n)
  if n == HOVER_FROM + 5 then
    local sel = Spring.GetSelectedUnits()
    local ud = sel[1] and UnitDefs[Spring.GetUnitDefID(sel[1])]
    log(ud ~= nil, "a unit is selected", ud and ud.name)
    local count = Spring.GetGameRulesParam("customGeovent_count") or 0
    log(count >= 1, "the gadget published the vent created at frame 1", count)
    log(WG.customGeoventSpots and #WG.customGeoventSpots >= 1, "the loader widget has it", WG.customGeoventSpots and #WG.customGeoventSpots)
    local mx, my = Spring.GetMouseState()
    local _, pos = Spring.TraceScreenRay(mx, my, true, true)
    if pos then
      local d = math.sqrt((pos[1] - vx) ^ 2 + (pos[3] - vz) ^ 2)
      log(d < 60, "the mouse is over the vent", string.format("%.0f elmos off", d))
    else
      log(false, "the mouse is over the vent", "ray misses the ground")
    end
  end
  if n == CLICK_AT and not clicked then
    clicked = true
    local mx, my = Spring.GetMouseState()
    local _, activeCmd = Spring.GetActiveCommand()
    local sel = Spring.GetSelectedUnits()
    local geo
    for _, uID in ipairs(sel) do
      for _, bo in ipairs(UnitDefs[Spring.GetUnitDefID(uID)].buildOptions or {}) do
        if UnitDefs[bo].needGeo then geo = UnitDefs[bo].name end
      end
    end
    local _, pos = Spring.TraceScreenRay(mx, my, true, true)
    if geo then
      local gd = UnitDefNames[geo].id
      local bx, by, bz = Spring.Pos2BuildPos(gd, vx, Spring.GetGroundHeight(vx, vz), vz, 0)
      Spring.Echo(string.format("[GEOPROBE] TestBuildOrder(%s at %.0f,%.0f) = %s", geo, bx, bz, tostring(Spring.TestBuildOrder(gd, bx, by, bz, 0))))
    end
    Spring.Echo("[GEOPROBE] before click: activeCmd=" .. tostring(activeCmd) .. " selected=" .. #sel .. " geoOption=" .. tostring(geo)
      .. " vents=" .. tostring(WG.customGeoventSpots and #WG.customGeoventSpots) .. " mouse=" .. mx .. "," .. my
      .. " ground=" .. (pos and string.format("%.0f,%.0f", pos[1], pos[3]) or "nil"))
    -- the snapping widget's own call-ins (this handler has no MousePress entry point to call)
    local snap
    for _, w in ipairs(widgetHandler.widgets or {}) do
      if w.whInfo and w.whInfo.name == "Metal Maker Placement Snapping" then snap = w end
    end
    log(snap ~= nil, "the snapping widget is loaded")
    local took = snap and snap:MousePress(mx, my, 3)
    if snap then snap:MouseRelease(mx, my, 3) end
    log(took == true, "the snapping widget took the right-click", tostring(took))
  end
  if n == CHECK_AT then
    local ok = false
    for _, uID in ipairs(Spring.GetSelectedUnits()) do
      for _, cmd in ipairs(Spring.GetUnitCommands(uID, -1) or {}) do
        if cmd.id < 0 and UnitDefs[-cmd.id] and UnitDefs[-cmd.id].needGeo then
          local d = math.sqrt((cmd.params[1] - vx) ^ 2 + (cmd.params[3] - vz) ^ 2)
          log(d < 40, "the commander queued a geothermal plant on the vent", UnitDefs[-cmd.id].name, string.format("%.0f elmos off", d))
          ok = true
        end
      end
    end
    if not ok then
      log(false, "the commander queued a geothermal plant on the vent", "no such order")
      for _, uID in ipairs(Spring.GetSelectedUnits()) do
        local ids = {}
        for _, cmd in ipairs(Spring.GetUnitCommands(uID, -1) or {}) do
          local ud = cmd.id < 0 and UnitDefs[-cmd.id]
          ids[#ids + 1] = cmd.id .. (ud and (" " .. ud.name .. " needGeo=" .. tostring(ud.needGeo)) or "") .. " params=" .. table.concat(cmd.params or {}, "/")
        end
        Spring.Echo("[GEOPROBE] queue of " .. UnitDefs[Spring.GetUnitDefID(uID)].name .. ": " .. table.concat(ids, ","))
      end
    end
  end
end
