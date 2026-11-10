function gadget:GetInfo()
  return { name = "Geo Probe", layer = 1002, enabled = true }
end
-- GEOPROBE=1 run_win_visual.sh (with VISUAL=arm_commander VISUALSELECT=1): a geovent is created south of the lineup
-- at frame 1; the LuaUI half (luaui/widgets/zz_geo_probe.lua) parks the mouse on it with the commander selected, so
-- the screenshots show the geothermal plant's hover ghost, then right-clicks through the widget handler and checks
-- the commander's queue. Game rules param geoprobe_x/z tell the widget where the vent is.
local opt = Spring.GetModOptions() or {}
if not (opt.geoprobe and opt.geoprobe ~= "") then return end
if not gadgetHandler:IsSyncedCode() then return end

-- every build order the synced side accepts, with the frame: the LuaUI half's right-click order shows up here
function gadget:UnitCommand(unitID, unitDefID, teamID, cmdID, cmdParams, cmdOpts, cmdTag)
  if cmdID < 0 then
    Spring.Echo(string.format("[GEOPROBE] frame %d: build %s accepted for unit %d at (%.0f, %.0f)", Spring.GetGameFrame(),
      UnitDefs[-cmdID].name, unitID, cmdParams[1] or -1, cmdParams[3] or -1))
  end
end

function gadget:GameFrame(n)
  if n ~= 1 then return end
  local name = FeatureDefNames.geovent and "geovent"
  if not name then
    for _, fd in pairs(FeatureDefs) do
      if fd.geoThermal then name = fd.name break end
    end
  end
  local x, z = Game.mapSizeX / 2, Game.mapSizeZ * 0.62 + 400
  if not name then
    Spring.Echo("[GEOPROBE] FAIL no geoThermal feature def in this game or map")
    return
  end
  local fID = Spring.CreateFeature(name, x, Spring.GetGroundHeight(x, z), z, 0)
  Spring.SetGameRulesParam("geoprobe_x", x)
  Spring.SetGameRulesParam("geoprobe_z", z)
  Spring.Echo(string.format("[GEOPROBE] vent %s at (%.0f, %.0f) feature %s", name, x, z, tostring(fID)))
end
