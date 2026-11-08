function gadget:GetInfo()
  return { name = "Mex Probe", layer = 1005, enabled = true }
end

-- MEXPROBE=1 MAP=... MAPNAME=... run.sh: metal spots, building mask, mex output, moho over mex, geovents.
-- Logs "[PROBE] mex ..." lines. TestBuildOrder: 0 = blocked, 1 = blocked by a feature (reclaimable), 2 = free.
if not gadgetHandler:IsSyncedCode() or not (Spring.GetModOptions() or {}).mexprobe then return end

local E = function(...) Spring.Echo("[PROBE] mex " .. string.format(...)) end
local mex, moho, llt = UnitDefNames["arm_t1_eco_metalextractor"].id, UnitDefNames["arm_t2_eco_mohomine"].id, UnitDefNames["arm_t1_def_llt"].id
local spot, mexID, mohoID, metal0, settarget

function gadget:GameFrame(n)
  if n == 30 then
    Spring.SendCommands("cheat 1")
    local count = Spring.GetGameRulesParam("metalSpot_count") or 0
    E("spots %d value %.3f players %s geovents %s", count, Spring.GetGameRulesParam("metalSpot_value") or -1,
      tostring(Spring.GetGameRulesParam("metalSpot_players")), tostring(Spring.GetGameRulesParam("customGeovent_count")))
    local pts = {}
    for i = 1, count do pts[i] = { Spring.GetGameRulesParam("metalSpot_" .. i .. "_x"), Spring.GetGameRulesParam("metalSpot_" .. i .. "_z") } end
    for i = 1, count do
      local best = 1e9
      for j = 1, count do
        if i ~= j then best = math.min(best, math.sqrt((pts[i][1] - pts[j][1]) ^ 2 + (pts[i][2] - pts[j][2]) ^ 2)) end
      end
      -- how far the spot is from the metal-weighted centre of the patch within 8 squares
      local sw, sx, sz = 0, 0, 0
      local qx, qz = math.floor(pts[i][1] / 16), math.floor(pts[i][2] / 16)
      for dz = -8, 8 do for dx = -8, 8 do
        local m = Spring.GetMetalAmount(qx + dx, qz + dz) or 0
        if m >= 0.1 then sw, sx, sz = sw + m, sx + m * ((qx + dx) * 16 + 8), sz + m * ((qz + dz) * 16 + 8) end
      end end
      local off = sw > 0 and math.sqrt((sx / sw - pts[i][1]) ^ 2 + (sz / sw - pts[i][2]) ^ 2) or -1
      E("spot %d at %d,%d nearest other %d off-centre %.1f", i, pts[i][1], pts[i][2], best, off)
    end
    -- a spot on dry land
    for i = 1, count do
      local x, z = Spring.GetGameRulesParam("metalSpot_" .. i .. "_x"), Spring.GetGameRulesParam("metalSpot_" .. i .. "_z")
      if Spring.GetGroundHeight(x, z) > 5 then spot = { x = x, z = z }; break end
    end
    if not spot then E("no dry spot"); return end
    local y = Spring.GetGroundHeight(spot.x, spot.z)
    E("spot at %d,%d", spot.x, spot.z)
    for _, d in ipairs({ mex, moho }) do
      local bx, _, bz = Spring.Pos2BuildPos(d, spot.x, y, spot.z, 0)
      E("build pos of %s on the spot: %+d,%+d from the spot (want +0,+0)", UnitDefs[d].name, bx - spot.x, bz - spot.z)
    end
    E("test mex on spot %d (want 2)", Spring.TestBuildOrder(mex, spot.x, y, spot.z, 0))
    E("test moho on spot %d (want 2)", Spring.TestBuildOrder(moho, spot.x, y, spot.z, 0))
    E("test mex 200 elmos off the spot %d (want 0)", Spring.TestBuildOrder(mex, spot.x + 200, y, spot.z, 0))
    E("test LLT on spot %d (want 0)", Spring.TestBuildOrder(llt, spot.x, y, spot.z, 0))
    metal0 = select(4, Spring.GetTeamResources(0, "metal"))
    mexID = Spring.CreateUnit(mex, spot.x, y, spot.z, 0, 0)
  elseif n == 100 and mexID then
    local _, _, _, inc = Spring.GetTeamResources(0, "metal")
    E("mex metal param %.3f energy %.3f; team metal income %.3f -> %.3f", Spring.GetUnitRulesParam(mexID, "mex_metal") or -1,
      Spring.GetUnitRulesParam(mexID, "mex_energy") or -1, metal0 or -1, inc or -1)
    local y = Spring.GetGroundHeight(spot.x, spot.z)
    E("test moho over the mex %d (want 2)", Spring.TestBuildOrder(moho, spot.x, y, spot.z, 0))
    E("test 2nd mex over the mex %d (want 0)", Spring.TestBuildOrder(mex, spot.x, y, spot.z, 0))
    mohoID = Spring.CreateUnit(moho, spot.x, y, spot.z, 0, 0, true)   -- being built
  elseif n == 110 and mohoID then
    E("moho under construction: mex still alive %s", tostring(Spring.ValidUnitID(mexID)))
    Spring.SetUnitHealth(mohoID, { build = 1 })
  elseif n == 160 and mohoID then
    E("moho finished: mex alive %s, moho metal %.3f, features near the spot %d",
      tostring(Spring.ValidUnitID(mexID)), Spring.GetUnitRulesParam(mohoID, "mex_metal") or -1,
      #Spring.GetFeaturesInCylinder(spot.x, spot.z, 60))
    -- Set Target: a Flash told to target an enemy Peewee in range locks onto it (targetID rules param)
    local flash = Spring.CreateUnit("arm_t1_veh_flash", spot.x + 80, 0, spot.z + 40, 0, 0)   -- dry land by the spot
    local enemy = Spring.CreateUnit("arm_t1_bot_peewee", spot.x + 80, 0, spot.z + 180, 0, 1)
    settarget = { flash, enemy }
    Spring.SetGlobalLos(0, true)   -- the harness's teams don't get LOS updates; a player only targets what it sees
  elseif n == 190 and settarget then
    Spring.GiveOrderToUnit(settarget[1], 34923, { settarget[2] }, {})   -- once the enemy is in its LOS
  elseif n == 215 and settarget then
    local idx = -1
    for _, d in ipairs(Spring.GetUnitCmdDescs(settarget[1]) or {}) do
      if d.id == 34923 then idx = 1 end
    end
    E("set target: command on flash %s, targetID rules param %s (want %d)", idx == 1 and "yes" or "no",
      tostring((Spring.GetUnitRulesParam(settarget[1], "targetID"))), settarget[2])
    E("done")
  end
end
