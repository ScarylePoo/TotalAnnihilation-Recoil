function gadget:GetInfo()
  return { name = "InstanceVBOTable Probe", layer = 1008, enabled = true }
end

-- Unit test of modules/graphics/instancevbotable.lua (VBOPROBE=1 run.sh), no GPU needed: gl.GetVBO is stubbed with
-- a fake buffer that checks its arguments the way LuaVBOImpl::Upload does (a start index past the end of the Lua
-- table is an error), and Spring.ValidUnitID with a set of pretend units. Pushes unit-bound instances past the first
-- resize, "kills" some units without popping them (the leak that happens when an enemy dies in view), pushes past the
-- next resize so the compaction drops them, pops from the middle and the end, and checks after every step that the
-- four tables agree and that every instance still holds the data it was pushed with. Echoes [VBOPROBE] PASS / FAIL.
local opt = Spring.GetModOptions() or {}
if not opt.vboprobe then return end
if gadgetHandler:IsSyncedCode() then return end

local failures = {}
local function check(cond, msg)
  if not cond then failures[#failures + 1] = msg end
  return cond
end

local alive = {}
local realValidUnitID = Spring.ValidUnitID

-- fake gl.GetVBO
local function FakeVBO()
  local vbo = { defined = 0 }
  function vbo:Define(n, layout) self.defined = n end
  function vbo:Delete() self.deleted = true end
  function vbo:GetID() return 1 end
  function vbo:Upload(tbl, attrib, elemOffset, luaStart, luaFinish)
    if luaStart and luaStart > #tbl then
      error(("[LuaVBOImpl::Upload] Invalid luaStartIndex [%d] exceeds table size [%d]"):format(luaStart, #tbl))
    end
    if luaFinish and luaFinish > #tbl then
      error(("[LuaVBOImpl::Upload] Invalid luaFinishIndex [%d] exceeds table size [%d]"):format(luaFinish, #tbl))
    end
    self.uploads = (self.uploads or 0) + 1
  end
  function vbo:InstanceDataFromUnitIDs(ids, attrib, idx)
    local list = type(ids) == "table" and ids or { ids }
    for _, id in ipairs(list) do
      if not alive[id] then error("InstanceDataFromUnitIDs: invalid unit " .. tostring(id)) end
    end
  end
  function vbo:InstanceDataFromFeatureIDs() end
  return vbo
end

local function run()
  gl = gl or {}
  GL = GL or {}
  GL.ARRAY_BUFFER = GL.ARRAY_BUFFER or 0x8892
  GL.UNSIGNED_INT = GL.UNSIGNED_INT or 0x1405
  local realGetVBO = gl.GetVBO
  gl.GetVBO = function() return FakeVBO() end
  Spring.ValidUnitID = function(id) return alive[id] == true end

  -- VBOPROBE=<path in the probe mod> tests another copy of the module (e.g. the old one, to see the test catch its bugs)
  local MODULE = (opt.vboprobe ~= "1" and tostring(opt.vboprobe)) or "modules/graphics/instancevbotable.lua"
  local IVT = VFS.Include(MODULE)
  local layout = {
    { id = 1, name = "a", size = 4 },
    { id = 2, name = "b", size = 4 },
    { id = 3, name = "instData", type = GL.UNSIGNED_INT, size = 4 },
  }
  local iT = IVT.makeInstanceVBOTable(layout, 16, "probe", 3)
  check(iT ~= nil, "makeInstanceVBOTable returned nil")
  local STEP = iT.instanceStep
  check(STEP == 12, "instanceStep " .. tostring(STEP))

  local pushed = {}  -- instanceID -> { unit = u, first = value }
  local function data(u)
    local t = {}
    for i = 1, STEP do t[i] = u * 100 + i end
    return t
  end
  local function push(u)
    alive[u] = true
    local id = "u" .. u
    local ok, err = pcall(IVT.pushElementInstance, iT, data(u), id, true, nil, u)
    check(ok, "push " .. id .. ": " .. tostring(err))
    pushed[id] = { unit = u, first = u * 100 + 1 }
  end
  local function pop(id)
    local ok, err = pcall(IVT.popElementInstance, iT, id)
    check(ok, "pop " .. id .. ": " .. tostring(err))
    pushed[id] = nil
  end
  local function consistent(where)
    local n = iT.usedElements
    -- instanceData is pre-filled to maxElements and never shrinks; it must only cover the used part without holes
    check(#iT.instanceData >= n * STEP, where .. ": #instanceData " .. #iT.instanceData .. " vs " .. n * STEP)
    for i = 1, n * STEP do
      if iT.instanceData[i] == nil then check(false, where .. ": hole in instanceData at " .. i) break end
    end
    local count = 0
    for id, idx in pairs(iT.instanceIDtoIndex) do
      count = count + 1
      check(iT.indextoInstanceID[idx] == id, where .. ": indextoInstanceID[" .. idx .. "] ~= " .. id)
      local p = pushed[id]
      if check(p ~= nil, where .. ": unknown instance " .. id .. " in table") then
        check(iT.indextoUnitID[idx] == p.unit, where .. ": unit of " .. id .. " is " .. tostring(iT.indextoUnitID[idx]))
        check(iT.instanceData[(idx - 1) * STEP + 1] == p.first,
          where .. ": data of " .. id .. " is " .. tostring(iT.instanceData[(idx - 1) * STEP + 1]) .. " not " .. p.first)
      end
    end
    check(count == n, where .. ": " .. count .. " ids for " .. n .. " elements")
    for i = 1, n do check(iT.indextoInstanceID[i] ~= nil, where .. ": nil element at " .. i) end
    check(iT.indextoInstanceID[n + 1] == nil, where .. ": stale element past the end")
  end

  for u = 1, 14 do push(u) end
  consistent("after 14 pushes")
  push(15); push(16)                       -- first resize (16 -> 32) with every unit alive
  consistent("after first resize")
  for u = 17, 20 do push(u) end
  alive[3], alive[7], alive[8] = nil, nil, nil   -- three units die without their instances being popped
  pushed["u3"], pushed["u7"], pushed["u8"] = nil, nil, nil
  for u = 21, 34 do push(u) end            -- second resize (32 -> 64) compacts the dead ones away
  consistent("after compacting resize")
  check(iT.usedElements == 31, "usedElements after compaction " .. iT.usedElements)
  check(iT.instanceIDtoIndex["u3"] == nil and iT.instanceIDtoIndex["u7"] == nil, "dead units survived the resize")
  pop("u34")                               -- the end element
  pop("u1")                                -- a middle element: u33 moves into slot 1
  pop("u20")
  consistent("after pops")
  -- the last element's unit dies without a pop; popping a middle one moves it back (the "zombie" case)
  local lastID = iT.indextoInstanceID[iT.usedElements]
  alive[pushed[lastID].unit] = nil
  pushed[lastID] = nil
  pop("u2")
  check(iT.instanceIDtoIndex[lastID] ~= nil, "moved-back dead element lost")
  -- the next resize must drop it, data of everyone else intact
  for u = 40, 78 do push(u) end            -- 27 + 39 pushes: the 37th hits 63 + 1 >= 64, the third resize (64 -> 128)
  consistent("after third resize")
  check(iT.instanceIDtoIndex[lastID] == nil, "zombie " .. tostring(lastID) .. " survived the third resize")
  -- push onto an existing id updates in place
  local before = iT.usedElements
  push(40)
  check(iT.usedElements == before, "update in place changed usedElements")
  consistent("after update")
  -- empty it out in random order
  local ids = {}
  for id in pairs(iT.instanceIDtoIndex) do ids[#ids + 1] = id end
  for i = #ids, 2, -1 do local j = math.random(i); ids[i], ids[j] = ids[j], ids[i] end
  for _, id in ipairs(ids) do pop(id) end
  check(iT.usedElements == 0, "not empty at the end: " .. iT.usedElements)

  gl.GetVBO = realGetVBO
  Spring.ValidUnitID = realValidUnitID
end

function gadget:GameFrame(n)
  if n ~= 3 then return end
  local ok, err = pcall(run)
  if not ok then failures[#failures + 1] = "error: " .. tostring(err) end
  if #failures == 0 then
    Spring.Echo("[VBOPROBE] PASS")
  else
    for i = 1, math.min(#failures, 25) do Spring.Echo("[VBOPROBE] FAIL " .. failures[i]) end
    Spring.Echo("[VBOPROBE] " .. #failures .. " failures")
  end
  Spring.SendCommands("quitforce")
end
