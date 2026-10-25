function gadget:GetInfo()
  return { name = "Test Harness", layer = 1000, enabled = true }
end

-- Phases (frames relative to the end of spawning, S = 10 + #UnitDefs):
--   10 .. S-1  spawn one unitdef per frame for both teams (interleaved, so enemies are adjacent)
--   S+50       builders/factories get a build order, everyone else a fight order
--   S+1500     everything self-destructs (death scripts, explosions, wrecks)
--   S+1800     features are destroyed
--   S+1950     quit
local SPAWN0 = 10

if gadgetHandler:IsSyncedCode() then

local SIZE = Game.mapSizeX
local LAKE_X0, LAKE_X1 = SIZE * 0.55, SIZE * 0.95
local spawned = {}
local landIdx, seaIdx, nSpawned = 0, 0, 0

local function log(...) Spring.Echo("[HARNESS]", ...) end

function gadget:Initialize()
  Spring.SetHeightMapFunc(function()
    for x = 0, SIZE, 8 do
      for z = 0, Game.mapSizeZ, 8 do
        if x > LAKE_X0 and x < LAKE_X1 then Spring.SetHeightMap(x, z, -60) end
      end
    end
  end)
end

local function isWaterUnit(ud)
  if ud.minWaterDepth and ud.minWaterDepth > 0 then return true end
  local md = ud.moveDef
  local n = md and md.name and md.name:lower() or ""
  if n:find("ship") or n:find("boat") or n:find("sub") then return true end
  return false
end

local function SpawnOne(udid)
  local ud = UnitDefs[udid]
  log("spawn", udid, ud.name)
  for team = 0, 1 do
    local x, z
    if isWaterUnit(ud) then
      x = LAKE_X0 + 150 + (seaIdx % 10) * 110
      z = 200 + math.floor(seaIdx / 10) * 110
      seaIdx = seaIdx + 1
    else
      x = 150 + (landIdx % 22) * 110
      z = 200 + math.floor(landIdx / 22) * 110
      landIdx = landIdx + 1
    end
    local ok, uid = pcall(Spring.CreateUnit, udid, x, Spring.GetGroundHeight(x, z), z, 0, team)
    if not ok or not uid then
      log("SPAWN FAIL", ud.name, tostring(uid))
    else
      spawned[#spawned + 1] = uid
      nSpawned = nSpawned + 1
    end
  end
end

function gadget:GameFrame(frame)
  if frame >= SPAWN0 and frame < SPAWN0 + #UnitDefs then
    SpawnOne(frame - SPAWN0 + 1)
    return
  end
  local f = frame - (SPAWN0 + #UnitDefs)
  if f == 0 then
    log("spawned", nSpawned, "units of", #UnitDefs, "defs")
  elseif f == 50 then
    for _, uid in ipairs(spawned) do
      if Spring.ValidUnitID(uid) then
        local ud = UnitDefs[Spring.GetUnitDefID(uid)]
        local x, y, z = Spring.GetUnitPosition(uid)
        if ud.isFactory and ud.buildOptions[1] then
          Spring.GiveOrderToUnit(uid, -ud.buildOptions[1], {}, {})
        elseif ud.isBuilder and ud.buildOptions[1] and ud.canMove then
          Spring.GiveOrderToUnit(uid, -ud.buildOptions[1], {x + 60, y, z + 60, 0}, {})
        elseif ud.canMove then
          Spring.GiveOrderToUnit(uid, CMD.FIGHT, {SIZE / 2, 0, Game.mapSizeZ / 2}, {})
        end
        Spring.GiveOrderToUnit(uid, CMD.FIRE_STATE, {2}, {})
      end
    end
    log("orders given")
  elseif f == 1500 then
    local all = Spring.GetAllUnits()
    for _, uid in ipairs(all) do Spring.DestroyUnit(uid, true) end
    log("destroyed", #all)
  elseif f == 1800 then
    local all = Spring.GetAllFeatures()
    log("features alive", #all)
    for _, fid in ipairs(all) do Spring.DestroyFeature(fid) end
  elseif f == 1900 then
    log("DONE")
  end
end

else

function gadget:Initialize()
  Spring.SendCommands("cheat 1", "setmaxspeed 200", "setminspeed 200")
end

function gadget:GameFrame(frame)
  if frame == SPAWN0 + #UnitDefs + 1950 then Spring.SendCommands("quitforce") end
end

end
