function gadget:GetInfo()
  return { name = "Visual Probe", layer = 1006, enabled = true }
end

-- Weapon visuals check (VISUAL="unit1,unit2,..." tools/headless-test/run.sh, graphical engine). Lines the units up,
-- gives team 0 unlimited energy/metal, makes them attack the ground in front of them over and over, points the camera
-- at the line from game height, takes screenshots (writedir/screenshots), quits. VISUALZOOM sets the camera height.
local opt = Spring.GetModOptions() or {}
if not opt.visualunits then return end

local SPACING = 150

local function lineup()
  local list = {}
  for name in tostring(opt.visualunits):gmatch("[^,]+") do
    local ud = UnitDefNames[name:lower()]
    if ud then list[#list + 1] = ud end
  end
  return list
end

local function attackDist(ud)
  local r = 300
  if ud.weapons[1] then r = WeaponDefs[ud.weapons[1].weaponDef].range end
  return math.max(120, math.min(r * 0.85, tonumber(opt.visualdist) or 420))
end

if gadgetHandler:IsSyncedCode() then

local units = {}
local shots = {}
function gadget:Initialize()
  for id = 1, #WeaponDefs do Script.SetWatchProjectile(id, true) end
end
function gadget:ProjectileCreated(proID, ownerID, weaponDefID)
  if ownerID then shots[ownerID] = (shots[ownerID] or 0) + 1 end
end

function gadget:GameFrame(n)
  if n == 2 then
    Spring.SendCommands("cheat 1", "godmode 1")
    for _, t in ipairs(Spring.GetTeamList()) do
      Spring.SetTeamResource(t, "es", 1e7) Spring.SetTeamResource(t, "e", 1e7)
      Spring.SetTeamResource(t, "ms", 1e7) Spring.SetTeamResource(t, "m", 1e7)
    end
    -- an enemy far away, so the game does not offer a surrender vote over the view
    Spring.CreateUnit("core_commander", Game.mapSizeX - 200, 0, 200, "south", 1)
    local list = lineup()
    local x0 = Game.mapSizeX / 2 - (#list - 1) * SPACING / 2
    local z = Game.mapSizeZ * 0.62
    for i, ud in ipairs(list) do
      local x = x0 + (i - 1) * SPACING
      local id = Spring.CreateUnit(ud.name, x, Spring.GetGroundHeight(x, z), z, "north", 0)
      if id then
        units[#units + 1] = { id = id, x = x, z = z - attackDist(ud) }
      else
        Spring.Echo("[VISUAL] spawn failed " .. ud.name)
      end
    end
  end
  if n % 30 == 0 and n > 0 then
    local p = Spring.GetProjectilesInRectangle(0, 0, Game.mapSizeX, Game.mapSizeZ)
    local cmds = {}
    for _, u in ipairs(units) do
      local q = Spring.GetUnitCommands(u.id, 1)
      local gy = Spring.GetGroundHeight(u.x, u.z)
      local t = {}
      for w = 1, #(UnitDefs[Spring.GetUnitDefID(u.id)].weapons) do
        local px, py, pz = Spring.GetUnitWeaponVectors(u.id, w)
        t[#t + 1] = ("w%d src=%.1f/ground=%.1f"):format(w, py or -1, Spring.GetGroundHeight(px or 0, pz or 0))
        t[#t + 1] = ("w%d tgt=%s rng=%s lof=%s"):format(w, tostring(Spring.GetUnitWeaponTestTarget(u.id, w, u.x, gy, u.z)),
          tostring(Spring.GetUnitWeaponTestRange(u.id, w, u.x, gy, u.z)), tostring(Spring.GetUnitWeaponHaveFreeLineOfFire(u.id, w, nil, nil, nil, u.x, gy, u.z)))
      end
      cmds[#cmds + 1] = UnitDefs[Spring.GetUnitDefID(u.id)].name .. ":" .. tostring(q and q[1] and q[1].id) .. ":" .. (shots[u.id] or 0) .. "(" .. table.concat(t, ",") .. ")"
    end
    Spring.Echo("[VISUAL] frame " .. n .. " projectiles " .. #p .. " " .. table.concat(cmds, " "))
  end
  if n >= 30 then
    for _, u in ipairs(units) do
      Spring.SetTeamResource(0, "e", 1e7)
      if n % 90 == 30 then
        Spring.GiveOrderToUnit(u.id, CMD.ATTACK, { u.x, Spring.GetGroundHeight(u.x, u.z), u.z }, {})
      end
    end
  end
end

else  -- unsynced: camera and screenshots

local list, cx, cz, far
local pending, draws, taken, quitting = nil, 0, 0, false
-- screenshots from the draw call-in so each one is a freshly rendered frame
-- The software renderer draws far slower than the sim runs, so from frame SLOW the game runs at a crawl and a screenshot
-- is taken on each draw after the sim has moved on by STEP frames, NSHOTS times.
local SLOW, STEP, NSHOTS = 190, 1, 12
local lastShot = -100

function gadget:Initialize()
  list = lineup()
  local dmax = 0
  for _, ud in ipairs(list) do dmax = math.max(dmax, attackDist(ud)) end
  cx = Game.mapSizeX / 2
  cz = Game.mapSizeZ * 0.62 - dmax * 0.45
  far = tonumber(opt.visualzoom) or 700
end
function gadget:DrawScreenPost()  -- last draw call-in of the frame: projectiles are drawn by then
  draws = draws + 1
  local n = Spring.GetGameFrame()
  if n >= SLOW + 5 and taken < NSHOTS and n - lastShot >= STEP then
    Spring.SendCommands("screenshot png")
    taken = taken + 1
    lastShot = n
  end
end

function gadget:GameFrame(n)
  if n == 20 then
    Spring.SendCommands("luaui disable", "console 0")
  end
  if n >= 20 and n < 60 then
    Spring.SetCameraState({ name = "spring", mode = 2, px = cx, py = Spring.GetGroundHeight(cx, cz), pz = cz,
      dist = far, rx = 2.35, ry = math.pi, rz = 0, fov = 45 }, 0)
  end
  -- (no slow motion: each drawn frame is a new sim state, which is what the screenshots need)
  if taken >= NSHOTS and not quitting then
    quitting = true
    Spring.Echo("[VISUAL] draw frames " .. draws .. ", shots taken " .. taken)
    Spring.Echo("[VISUAL] camera " .. table.concat((function()
      local t = {} for k, v in pairs(Spring.GetCameraState()) do t[#t + 1] = k .. "=" .. tostring(v) end return t end)(), " "))
    Spring.SendCommands("quitforce")
  end
end

end
