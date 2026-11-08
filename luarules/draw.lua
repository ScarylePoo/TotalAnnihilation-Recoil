-- TA:Recoil: the shared helpers in Common/ (table.copy, Spring.Utilities, ...) for every gadget, as LuaUI
-- (luaui/main.lua) and Splinter Faction's LuaRules already have them; SF gadgets and configs use them.
VFS.Include("init.lua", nil, VFS.ZIP)
Spring.Utilities = Spring.Utilities or {}
VFS.Include("LuaRules/Utilities/tablefunctions.lua", nil, VFS.ZIP)  -- SF's Spring.Utilities.CopyTable etc. (SF gadgets)
VFS.Include("LuaRules/Utilities/unitTypeChecker.lua", nil, VFS.ZIP)  -- SF's Spring.Utilities.getMovetype etc. (LUPS)
VFS.Include("LuaGadgets/gadgets.lua",nil, VFS.BASE)
