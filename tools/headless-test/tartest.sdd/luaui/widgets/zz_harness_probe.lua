function widget:GetInfo() return { name = "Harness Probe", layer = 99999, enabled = true, handler = true } end
function widget:GameFrame(f)
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
