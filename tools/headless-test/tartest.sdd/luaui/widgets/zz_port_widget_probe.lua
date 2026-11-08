function widget:GetInfo() return { name = "Port Widget Probe", layer = 99998, enabled = true, handler = true } end
-- PORTPROBE=1 run.sh, the player's side: see luarules/gadgets/zz_port_probe.lua
if not (Spring.GetModOptions() or {}).portprobe then return false end

local E = function(...) Spring.Echo("[PROBE] port " .. string.format(...)) end
local function P(k) return Spring.GetGameRulesParam("portprobe_" .. k) end
local start, splitClicks
-- orders given from LuaUI reach the simulation ~30 frames later on headless, so the steps are far apart

function widget:GameFrame(f)
  if not start and P("ready") then start = f end
  if not start then return end
  local t = f - start
  if t == 2 then
    local names = {}
    for _, w in ipairs(widgetHandler.widgets) do names[w.whInfo.name] = true end
    local want = { "CommandInsert", "Build Order Splitter", "Show Builder Queue", "ReclaimInfo", "Stop Self-D",
      "Persistent Build Spacing", "Mouse Buildspacing", "Auto First Build Facing", "ImmobileBuilder", "Load Own Moving",
      "State Reverse Toggle", "QueueCopypasta", "Constructor locater", "AllyCursors", "Ally Selected Units",
      "Spectate Selected", "Player-TV", "CameraShake" }
    local missing = {}
    for _, n in ipairs(want) do if not names[n] then missing[#missing + 1] = n end end
    E("widgets missing: %s; Stall Assist on: %s (want none; false)", #missing == 0 and "none" or table.concat(missing, ", "),
      tostring(names["Stall Assist"] or false))
    E("advplayerlist_api %s, position %s", tostring(WG['advplayerlist_api'] ~= nil),
      WG['advplayerlist_api'] and table.concat(WG['advplayerlist_api'].GetPosition(), ",") or "-")
    -- team colours as the player sees them
    for _, team in ipairs({ 0, 1, 2 }) do
      E("LuaUI reads team %d colour param %s; team colour %.2f,%.2f,%.2f", team,
        tostring((Spring.GetTeamRulesParam(team, "AutoTeamColorRed"))), Spring.GetTeamColor(team))
    end
    -- stockpile: 100 asked for, capped at 10; then 2 more after a cancel of 5
    local silo = P("silo")
    Spring.GiveOrderToUnit(silo, CMD.STOCKPILE, {}, { "ctrl", "shift" })
  elseif t == 40 then
    local silo = P("silo")
    local s, q = Spring.GetUnitStockpile(silo)
    E("silo after asking 100: stock %d queued %d (want 0 10)", s, q)
    Spring.GiveOrderToUnit(silo, CMD.STOCKPILE, {}, { "shift", "right" })
  elseif t == 80 then
    local s, q = Spring.GetUnitStockpile(P("silo"))
    E("silo after removing 5: stock %d queued %d (want 0 5)", s, q)
    -- priority: high on a constructor
    Spring.GiveOrderToUnit(P("con1"), 34220, { 2 }, 0)
  elseif t == 120 then
    local idx = Spring.FindUnitCmdDesc(P("con1"), 34220)
    local d = idx and Spring.GetUnitCmdDescs(P("con1"), idx, idx)[1]
    E("con priority state %s (want 2)", d and tostring(d.params[1]) or "?")
    -- build order splitter (through Spring.GiveOrder: does it reach CommandNotify?)
    Spring.SelectUnitArray({ P("con1"), P("con2") })
    local def = UnitDefNames["arm_t1_eco_solarcollector"] or UnitDefNames["arm_t1_eco_solar"]
    if def then
      for i = 0, 3 do
        local x, z = 1500 + i * 100, 600
        Spring.GiveOrder(-def.id, { x, Spring.GetGroundHeight(x, z), z, 0 }, { "shift" })
      end
    else
      E("no solar def")
    end
  elseif t == 160 then
    local function nb(id) local n = 0; for _, c in ipairs(Spring.GetUnitCommands(id, -1) or {}) do if c.id < 0 then n = n + 1 end end; return n end
    E("split via Spring.GiveOrder: con1 %d con2 %d buildings", nb(P("con1")), nb(P("con2")))
    Spring.GiveOrderToUnit(P("con1"), CMD.STOP, {}, 0)
    Spring.GiveOrderToUnit(P("con2"), CMD.STOP, {}, 0)
  elseif t == 200 then
    -- a click goes through CommandNotify: call the splitter's as the engine would, 4 shift-clicked solars in one frame
    local function q(id) local o = {}; for _, c in ipairs(Spring.GetUnitCommands(id, -1) or {}) do o[#o + 1] = c.id .. "@" .. math.floor(c.params[1] or 0) .. "," .. math.floor(c.params[3] or 0) end; return table.concat(o, " ") end
    E("before clicks: con1 [%s] con2 [%s] selected %d", q(P("con1")), q(P("con2")), #Spring.GetSelectedUnits())
    local splitter
    for _, w in ipairs(widgetHandler.widgets) do if w.whInfo.name == "Build Order Splitter" then splitter = w end end
    local def = UnitDefNames["arm_t1_eco_solarcollector"]
    local used = 0
    for i = 0, 3 do
      local x, z = 1500 + i * 100, 800
      if splitter:CommandNotify(-def.id, { x, Spring.GetGroundHeight(x, z), z, 0 }, { shift = true, coded = CMD.OPT_SHIFT }) then used = used + 1 end
    end
    splitClicks = used
  elseif t == 240 then
    local function nb(id) local n = 0; for _, c in ipairs(Spring.GetUnitCommands(id, -1) or {}) do if c.id < 0 then n = n + 1 end end; return n end
    local function q(id) local o = {}; for _, c in ipairs(Spring.GetUnitCommands(id, -1) or {}) do o[#o + 1] = c.id .. "@" .. math.floor(c.params[1] or 0) .. "," .. math.floor(c.params[3] or 0) end; return table.concat(o, " ") end
    E("after clicks: con1 [%s] con2 [%s]", q(P("con1")), q(P("con2")))
    E("split via clicks: taken %d, con1 %d con2 %d buildings (want 4, 2 2)", splitClicks or -1, nb(P("con1")), nb(P("con2")))
    -- give a unit with orders to an ally, through the share window's path
    local gift = P("gift")
    Spring.GiveOrderToUnit(gift, CMD.MOVE, { 1200, 100, 1200 }, 0)
    Spring.GiveOrderToUnit(gift, CMD.MOVE, { 1400, 100, 1400 }, { "shift" })
    Spring.SelectUnitArray({ gift })
  elseif t == 280 then
    local gift = P("gift")
    local tokens = {}
    for _, cmd in ipairs(Spring.GetUnitCommands(gift, -1) or {}) do
      local fields = { tostring(cmd.id) }
      for _, p in ipairs(cmd.params or {}) do fields[#fields + 1] = tostring(p) end
      local o = cmd.options
      fields[#fields + 1] = "OPTS:" .. tostring(type(o) == "table" and (o.coded or 0) or o or 0)
      tokens[#tokens + 1] = table.concat(fields, ",")
    end
    Spring.SendLuaRulesMsg("ShareOrders:" .. gift .. ":2:" .. table.concat(tokens, "|"))
    Spring.ShareResources(2, "units")
  end
end
