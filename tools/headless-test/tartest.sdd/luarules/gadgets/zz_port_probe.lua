function gadget:GetInfo()
  return { name = "Port Probe", layer = 1005, enabled = true }
end

-- PORTPROBE=1 run.sh: the widgets and gadgets brought over from Splinter Faction (Nov 2026). Synced half: spawns the
-- units and checks the gadgets; the LuaUI half (luaui/widgets/zz_port_widget_probe.lua) gives the player's orders.
-- Team 2 is an ally of team 0 (run.sh adds it). Logs "[PROBE] port ..." lines.
if not gadgetHandler:IsSyncedCode() or not (Spring.GetModOptions() or {}).portprobe then return end

local E = function(...) Spring.Echo("[PROBE] port " .. string.format(...)) end
local D = UnitDefNames
local CMD_PRIORITY = 34220
local u = {}

local function Make(name, x, z, team, nanoframe)
  local id = Spring.CreateUnit(name, x, Spring.GetGroundHeight(x, z), z, 0, team, nanoframe)
  return id
end

function gadget:GameFrame(n)
  if n == 20 then
    Spring.SendCommands("cheat 1")
    for _, t in ipairs({ 0, 1, 2 }) do
      E("team %d colour params pal1 %s,%s,%s pal2 %s", t, tostring(Spring.GetTeamRulesParam(t, "AutoTeamColorRed")),
        tostring(Spring.GetTeamRulesParam(t, "AutoTeamColorGreen")), tostring(Spring.GetTeamRulesParam(t, "AutoTeamColorBlue")),
        tostring(Spring.GetTeamRulesParam(t, "AutoTeamColorRed2")))
    end
    u.con1 = Make("arm_t1_bot_constructor", 900, 900, 0)
    u.con2 = Make("arm_t1_bot_constructor", 950, 900, 0)
    u.peewee = Make("arm_t1_bot_peewee", 1000, 900, 0)
    u.lab = Make("arm_t1_lab_kbotlab", 1300, 1300, 0)
    u.silo = Make("arm_t2_def_retaliator", 700, 1400, 0)
    u.gift = Make("arm_t1_bot_peewee", 1100, 900, 0)
    u.enemyFrame = Make("core_t1_bot_ak", 1000, 1000, 1, true)
    u.ownFrame = Make("arm_t1_bot_peewee", 1050, 1050, 0, true)
    for k, v in pairs(u) do Spring.SetGameRulesParam("portprobe_" .. k, v) end
    Spring.SetGameRulesParam("portprobe_ready", 1)
  elseif n == 25 then
    E("priority button: con %s lab %s peewee %s (want yes yes no)",
      Spring.FindUnitCmdDesc(u.con1, CMD_PRIORITY) and "yes" or "no", Spring.FindUnitCmdDesc(u.lab, CMD_PRIORITY) and "yes" or "no",
      Spring.FindUnitCmdDesc(u.peewee, CMD_PRIORITY) and "yes" or "no")
    -- reclaiming someone else's nanoframe is refused, your own is not
    Spring.GiveOrderToUnit(u.con1, CMD.RECLAIM, { u.enemyFrame }, 0)
    local q1 = #(Spring.GetUnitCommands(u.con1, -1) or {})
    Spring.GiveOrderToUnit(u.con2, CMD.RECLAIM, { u.ownFrame }, 0)
    local q2 = #(Spring.GetUnitCommands(u.con2, -1) or {})
    E("reclaim enemy nanoframe queued %d (want 0), own nanoframe queued %d (want 1)", q1, q2)
    Spring.GiveOrderToUnit(u.con1, CMD.STOP, {}, 0)
    Spring.GiveOrderToUnit(u.con2, CMD.STOP, {}, 0)
    -- a unit out of a factory does not block others for a while
    Spring.GiveOrderToUnit(u.lab, -D["arm_t1_bot_peewee"].id, {}, 0)
  end
end

function gadget:UnitFromFactory(unitID, unitDefID, teamID, builderID)
  local blocking = Spring.GetUnitBlocking(unitID)
  E("unit from factory: blocking %s (want false)", tostring(blocking))
end

function gadget:UnitGiven(unitID, unitDefID, newTeam, oldTeam)
  if unitID == u.gift then
    -- the preserve-orders gadget re-issues on its own UnitGiven; read the queue a frame later
    u.giftCheck = Spring.GetGameFrame() + 2
  end
end

local orig = gadget.GameFrame
function gadget:GameFrame(n)
  orig(self, n)
  if n == 900 then Spring.SendCommands("quitforce") end
  if u.giftCheck and n == u.giftCheck then
    local q = Spring.GetUnitCommands(u.gift, -1) or {}
    local ids = {}
    for _, c in ipairs(q) do ids[#ids + 1] = c.id .. "@" .. math.floor(c.params[1] or 0) end
    E("given unit now team %d with %d orders: %s (want 2: 10@1200 10@1400)", Spring.GetUnitTeam(u.gift), #q, table.concat(ids, " "))
  end
end

