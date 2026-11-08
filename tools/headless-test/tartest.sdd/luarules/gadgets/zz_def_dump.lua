function gadget:GetInfo()
  return { name = "Def Dump", layer = 1005, enabled = true }
end

-- Writes every runtime UnitDef and WeaponDef (as the engine resolved them, after all def post-processing) to the
-- infolog as DEFDUMP lines, then quits. Runs alone (DUMP=1 run.sh). tools/ta-data/defdump.py turns the lines into JSON
-- for before/after diffs and for the TA comparison (synced Lua has no io).
-- Line format: "DEFDUMP U|W <name> <key>=<value>" one per scalar field; nested tables are flattened with dots.
local opt = Spring.GetModOptions() or {}
if not opt.dumponly or not gadgetHandler:IsSyncedCode() then return end

local echo = Spring.Echo
local function out(kind, name, key, v)
  local t = type(v)
  if t == "number" or t == "boolean" or t == "string" then
    echo(("DEFDUMP %s %s %s=%s"):format(kind, name, key, tostring(v)))
  end
end

local function walk(kind, name, prefix, tbl, depth)
  if depth > 3 then return end
  for k, v in pairs(tbl) do
    local key = prefix and (prefix .. "." .. tostring(k)) or tostring(k)
    if type(v) == "table" then
      walk(kind, name, key, v, depth + 1)
    else
      out(kind, name, key, v)
    end
  end
end

local function dumpDef(kind, def)
  local name = def.name
  local ok = pcall(function()
    for k, v in def:pairs() do
      if type(v) == "table" then
        walk(kind, name, k, v, 1)
      else
        out(kind, name, k, v)
      end
    end
  end)
  if not ok then echo("DEFDUMP ERR " .. kind .. " " .. tostring(name)) end
end

function gadget:GameFrame(n)
  if n ~= 3 then return end
  for id = 1, #WeaponDefs do
    local wd = WeaponDefs[id]
    dumpDef("W", wd)
    -- damages are indexed by armor type number; name them
    for i = 0, #Game.armorTypes do
      local an = Game.armorTypes[i]
      if an and wd.damages[i] then out("W", wd.name, "dmg." .. an, wd.damages[i]) end
    end
  end
  for id = 1, #UnitDefs do dumpDef("U", UnitDefs[id]) end
  for id, fd in pairs(FeatureDefs) do  -- features: customParams only (normal maps etc.)
    for k, v in pairs(fd.customParams or {}) do out("F", fd.name, "customParams." .. k, v) end
  end
  echo("DEFDUMP END")
  Spring.SendCommands("quitforce")
end
