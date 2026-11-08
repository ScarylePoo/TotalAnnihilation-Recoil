function widget:GetInfo() return { name = "Harness Probe", layer = 99999, enabled = true, handler = true } end
local placementSeen, doneSeen
function widget:GameFrame(f)
  if f == 25 then   -- the loading screen's music carried into the game (LuaIntro music addon -> Slate Music)
    local played, total = Spring.GetSoundStreamTime()
    local st = WG.SlateMusic and WG.SlateMusic.GetStatus and WG.SlateMusic.GetStatus() or {}
    Spring.Echo(string.format("[PROBE] music stream %.1f / %.1f s, loadscreen track %s, Slate Music: %s - %s",
      played or -1, total or -1, Spring.GetConfigString("music_loadscreen_track", "?"), tostring(st.artist), tostring(st.title)))
  end
  if f == 20 then   -- KEYPROBE / any run: what a few keys are bound to
    for _, k in ipairs({ "y", "Ctrl+y", "Alt+s", "q", "esc", "f11" }) do
      local acts = {}
      for _, b in ipairs(Spring.GetKeyBindings(k) or {}) do acts[#acts + 1] = b.command or b[1] or "?" end
      Spring.Echo("[PROBE] keys " .. k .. " = " .. table.concat(acts, ", "))
    end
  end
  if not placementSeen and Spring.GetGameRulesParam("phase") == "placement" then
    -- run.sh STARTP: which widgets are up once start placement begins
    placementSeen = f
    local names = {}
    for _, w in ipairs(widgetHandler.widgets) do names[#names + 1] = w.whInfo.name end
    Spring.Echo("[PROBE] at placement (" .. #names .. "): " .. table.concat(names, ", ") .. "; WG.SlatePregame=" .. tostring(WG.SlatePregame))
  end
  if placementSeen and (Spring.GetModOptions() or {}).startprobe and f == placementSeen + 12 then
    -- run.sh STARTP: a player reads no other team's claims (allied params;
    -- in FFA nobody is an ally), only its own refusal notice
    local me, seen = Spring.GetMyTeamID(), {}
    for _, t in ipairs(Spring.GetTeamList()) do
      if t ~= me and not Spring.AreTeamsAllied(t, me) then
        for _, k in ipairs({"claimedSpot", "selectedSpot", "confirmedSpot", "refusedSpot", "refusedCount"}) do
          if Spring.GetTeamRulesParam(t, k) ~= nil then seen[#seen + 1] = t .. "." .. k end
        end
      end
    end
    for _, prm in ipairs(Spring.GetGameRulesParams() or {}) do
      local name = type(prm) == "table" and (prm.name or next(prm)) or tostring(prm)
      if tostring(name):lower():find("claim") then seen[#seen + 1] = "game." .. tostring(name) end
    end
    Spring.Echo("[HARNESS] START, " .. (#seen == 0 and "PASS" or "FAIL") .. ", LuaUI of team " .. me .. " reads no opponent's spot params " .. table.concat(seen, " "))
    if Spring.GetGameRulesParam("isFFA") == 1 then
      Spring.Echo("[HARNESS] START, " .. (Spring.GetTeamRulesParam(me, "refusedCount") == 1 and "PASS" or "FAIL") .. ", LuaUI of team " .. me .. " reads its refusal notice, spot " .. tostring(Spring.GetTeamRulesParam(me, "refusedSpot")))
    end
  end
  if Spring.GetGameRulesParam("phase") == "done" then
    doneSeen = doneSeen or f
    if f == doneSeen + 10 then
      local up = {}
      for _, w in ipairs(widgetHandler.widgets) do
        local n = w.whInfo.name
        if n == "Slate Start Placement" or n == "Slate Faction Chooser" then up[#up + 1] = n end
      end
      Spring.Echo("[PROBE] after spawn: pregame widgets still up: " .. (#up > 0 and table.concat(up, ", ") or "none") .. "; WG.SlatePregame=" .. tostring(WG.SlatePregame))
    end
  end
  if f == 30 then
    local names = {}
    for _, w in ipairs(widgetHandler.widgets) do names[#names + 1] = w.whInfo.name end
    Spring.Echo("[PROBE] active (" .. #names .. "): " .. table.concat(names, ", "))
    local known = {}
    for name, ki in pairs(widgetHandler.knownWidgets or {}) do known[#known + 1] = name .. (ki.active and "+" or "-") end
    table.sort(known)
    Spring.Echo("[PROBE] known (" .. #known .. "): " .. table.concat(known, ", "))
    Spring.Echo("[PROBE] dirlist:", #VFS.DirList("LuaUI/Slate/Widgets/", "*.lua", VFS.ZIP_ONLY), #VFS.DirList("luaui/slate/widgets/", "*.lua"))
    Spring.Echo("[PROBE] RmlUi:", tostring(RmlUi), RmlUi and tostring(RmlUi.GetContext("shared")))
  end
end
