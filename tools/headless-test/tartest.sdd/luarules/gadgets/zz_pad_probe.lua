function gadget:GetInfo()
  return { name = "Air Pad Probe", layer = 1003, enabled = true }
end

-- Does luarules/gadgets/unit_air_pads.lua work? Runs alone (PADS=1 run.sh, which adds teams 2 (ally of 1) and 3-5 (own alliances: their pads are out of the
-- other tests' reach)). Every unit is immune unless a test says otherwise. "[PADLOG]" lines are the time series (health, state, height and distance to the
-- point, every second, in the infolog); "[HARNESS] PAD" lines are the verdicts. A plane counts as down when its origin is within 1 elmo of the point's piece.
local opt = Spring.GetModOptions() or {}
if not opt.padonly then return end

local CMD_PAD = 33791

if not gadgetHandler:IsSyncedCode() then
  -- the right click: DefaultCommand needs a selection, so it runs on team 0 (the player's) with units the synced side made
  local function Run(_, plane, hurt, pad, full)
    -- the global call-in is what the engine calls, through every gadget that has one
    local DC = _G.DefaultCommand
    Spring.SelectUnitArray({ plane })
    local n = #(Spring.GetSelectedUnits() or {})
    local onPadHurt = DC("unit", pad)
    local onPlane = DC("unit", plane)
    Spring.SelectUnitArray({ full })
    local onPadFull = DC("unit", pad)
    Spring.Echo("[HARNESS] PAD " .. ((n == 1 and onPadHurt == CMD_PAD and not onPlane and not onPadFull) and "PASS" or "FAIL") .. " rightclick DefaultCommand: selected " .. n .. " damaged plane on pad=" ..
      tostring(onPadHurt) .. " on non-pad=" .. tostring(onPlane) .. " full-health plane on pad=" .. tostring(onPadFull))
  end
  -- ---------------------------------------------------- the nano spray. Headless draws nothing: this checks what the emitter does, not how it looks.
  -- The synced side sends, every frame, who it sees being repaired (on deck, damaged, pad working): the set the emitter may spray for.
  Spring.SetConfigInt("MaxNanoParticles", 2000) -- 0 on headless, which would turn the spray off
  Spring.SetConfigInt("TeamNanoSpray", 1)
  local nowF, repairing, repairingPrev = 0, {}, {}
  local N = { emits = 0, illegal = 0, offPad = 0, offPlane = 0, wrongPiece = 0, maxPad = 0, maxAim = 0, maxAlive = 0, moving = 0, maxDrift = 0, maxSpeed = 0, teamBad = 0, teamChecks = 0, greenBad = 0, greenChecks = 0, wrongFrame = 0 }
  local firstBad = {}
  local expectFrames, emitFrames, names = {}, {}, {}
  local inFlight = {}
  local colourSince = 0
  local PIECES = { arm_t2_def_airrepairpad = { beam1 = true, beam2 = true }, core_t2_def_airrepairpad = { beam1 = true, beam2 = true }, arm_t2_sea_colossus = { radar = true }, core_t2_sea_hive = { dish = true } }
  local pieceSeen = {}
  local function Bad(what, s) N[what] = N[what] + 1; firstBad[what] = firstBad[what] or s end
  local function Report(ok, name, ...)
    local t = { ... }
    for i = 1, #t do t[i] = tostring(t[i]) end
    Spring.Echo("[HARNESS] PAD " .. (ok and "PASS " or "FAIL ") .. name .. " " .. table.concat(t, " "))
  end
  local function OnEmit(beam, particle, piece, sx, sy, sz, tx, ty, tz)
    local nano = GG.AirPadNano
    N.emits = N.emits + 1
    local key = beam.plane .. ":" .. beam.pad
    emitFrames[beam.plane] = (emitFrames[beam.plane] or 0) + 1
    if not repairing[key] and not repairingPrev[key] then Bad("illegal", "f=" .. nowF .. " " .. key) end
    if particle.born ~= nowF then Bad("wrongFrame", "born " .. particle.born .. " at " .. nowF) end
    local padDef = UnitDefs[Spring.GetUnitDefID(beam.pad)]
    local pieceName = Spring.GetUnitPieceList(beam.pad)[piece]
    pieceSeen[padDef.name .. "." .. tostring(pieceName)] = true
    if not PIECES[padDef.name][pieceName] then Bad("wrongPiece", padDef.name .. "." .. tostring(pieceName)) end
    local px, py, pz = Spring.GetUnitPosition(beam.pad)
    local dPad = math.sqrt((sx - px)^2 + (sy - py)^2 + (sz - pz)^2)
    N.maxPad = math.max(N.maxPad, dPad)
    if dPad > 90 then Bad("offPad", padDef.name .. " start " .. dPad .. " from pad") end
    local _, _, _, mx, my, mz = Spring.GetUnitPosition(beam.plane, true)
    local radius = Spring.GetUnitRadius(beam.plane)
    local dAim = math.sqrt((tx - mx)^2 + (ty - my)^2 + (tz - mz)^2)
    N.maxAim = math.max(N.maxAim, dAim / radius)
    if dAim > radius then Bad("offPlane", "aim " .. dAim .. " off a plane of radius " .. radius) end
    -- on a moving carrier: when it dies, is it at the plane, which has moved on by then?
    local vx, _, vz = Spring.GetUnitVelocity(beam.pad)
    local speed = math.sqrt(vx * vx + vz * vz)
    if speed > 1 and particle.dies - particle.born >= 3 then
      N.maxSpeed = math.max(N.maxSpeed, speed)
      inFlight[#inFlight + 1] = { beam = beam, particle = particle, radius = radius, length = math.sqrt((tx - sx)^2 + (ty - sy)^2 + (tz - sz)^2) }
    end
    N.maxAlive = math.max(N.maxAlive, (function() local c = 0; for _, b in pairs(nano.beams) do c = c + #b.particles end; return c end)())
  end
  local drawCells = {}
  local function OnDrawCell(_, plane, pad, name) drawCells[#drawCells + 1] = { plane = plane, pad = pad, name = name } end
  local function OnFrame(_, frame, list, deckCount)
    nowF = frame
    repairingPrev, repairing = repairing, {}
    for plane, pad in string.gmatch(list, "(%d+):(%d+)") do
      repairing[plane .. ":" .. pad] = true
      expectFrames[tonumber(plane)] = (expectFrames[tonumber(plane)] or 0) + 1
    end
    local nano = GG.AirPadNano
    if nano and not nano.onEmit then nano.onEmit = OnEmit end
    -- every beam alive has to be a repair going on
    for plane, beam in pairs(nano and nano.beams or {}) do
      local key = plane .. ":" .. beam.pad
      if not repairing[key] and not repairingPrev[key] then Bad("illegal", "beam open f=" .. frame .. " " .. key) end
      if frame - colourSince > 31 then
        local want, r, g, b
        if colourSince == 0 or N.colourMode ~= "green" then
          r, g, b = Spring.GetTeamColor(Spring.GetUnitTeam(beam.pad))
          N.teamChecks = N.teamChecks + 1
          -- it repaints once a second; a pad given to another team gets that long
          if math.abs(beam.r - r) + math.abs(beam.g - g) + math.abs(beam.b - b) > 0.01 then
            beam.wrongSince = beam.wrongSince or frame
            if frame - beam.wrongSince > 31 then Bad("teamBad", "plane " .. plane .. " " .. tostring(beam.r) .. " want " .. tostring(r)) end
          else
            beam.wrongSince = nil
          end
        else
          local ud = UnitDefs[Spring.GetUnitDefID(beam.pad)]
          N.greenChecks = N.greenChecks + 1
          if math.abs(beam.r - ud.nanoColorR) + math.abs(beam.g - ud.nanoColorG) + math.abs(beam.b - ud.nanoColorB) > 0.01 then Bad("greenBad", tostring(beam.r)) end
        end
      end
    end
    -- the draw call: one player's own repair and an enemy's, both on screen. Team 0 is the player's; team 1 is not allied
    if frame == 61 then Spring.SetCameraTarget(1800, 100, 10900, 0) end
    for _, c in ipairs(drawCells) do
      local beam = nano and nano.beams[c.plane]
      if beam then
        c.beamFrames = (c.beamFrames or 0) + 1
        c.drawn = beam.drawn or 0
        c.inView = c.inView or Spring.IsUnitInView(c.pad)
        c.los = c.los or Spring.IsUnitInLos(c.pad, Spring.GetLocalAllyTeamID()) or Spring.IsUnitInLos(c.plane, Spring.GetLocalAllyTeamID())
      end
    end
    if frame == 2400 then Spring.SetConfigInt("TeamNanoSpray", 0); N.colourMode = "green"; colourSince = frame end
    -- particles on a moving carrier, just before they die
    local i = 1
    while inFlight[i] do
      local f = inFlight[i]
      if frame >= f.particle.dies - 1 then
        if nano.beams[f.beam.plane] == f.beam then
          N.moving = N.moving + 1
          local px, py, pz = Spring.GetUnitPosition(f.beam.pad)
          local x, y, z = nano.Position(f.particle, px, py, pz, frame + 1)
          local _, _, _, mx, my, mz = Spring.GetUnitPosition(f.beam.plane, true)
          local drift = math.sqrt((x - mx)^2 + (y - my)^2 + (z - mz)^2)
          -- what it may be off by: where in the plane it aimed, and the random part of its direction
          N.maxDrift = math.max(N.maxDrift, drift - f.radius * 0.87 - f.length * 0.26)
        end
        table.remove(inFlight, i)
      else
        i = i + 1
      end
    end
  end
  local function OnEnd()
    local nano = GG.AirPadNano
    Report(N.emits > 0 and N.illegal == 0 and N.wrongFrame == 0, "nano_only_while_repairing", N.emits, "particles, illegal", N.illegal, firstBad.illegal or "")
    local worst, worstPlane = 2, nil
    local planes = 0
    for plane, count in pairs(expectFrames) do
      if count >= 45 then
        planes = planes + 1
        local ratio = (emitFrames[plane] or 0) / count
        if ratio < worst then worst, worstPlane = ratio, plane end
      end
    end
    Report(planes > 10 and worst > 0.75, "nano_sprays_all_through_the_repair", planes, "planes, worst particles per repairing frame", string.format("%.2f", worst), "plane", worstPlane)
    local seen = {}
    for k in pairs(pieceSeen) do seen[#seen + 1] = k end
    table.sort(seen)
    Report(N.wrongPiece == 0 and N.offPad == 0 and pieceSeen["arm_t2_def_airrepairpad.beam1"] and pieceSeen["arm_t2_def_airrepairpad.beam2"] and pieceSeen["core_t2_def_airrepairpad.beam1"] and pieceSeen["arm_t2_sea_colossus.radar"] and pieceSeen["core_t2_sea_hive.dish"], "nano_starts_on_the_pads_nano_piece",
      table.concat(seen, ","), string.format("furthest from pad origin %.0f", N.maxPad), firstBad.wrongPiece or "", firstBad.offPad or "")
    Report(N.offPlane == 0, "nano_aims_into_the_plane", string.format("furthest aim %.2f of plane radius", N.maxAim), firstBad.offPlane or "")
    Report(N.moving > 100 and N.maxDrift < 1 and N.maxSpeed > 1, "nano_reaches_the_plane_on_a_moving_carrier", N.moving, "particles followed", string.format("carrier up to %.2f e/f, worst %.2f elmos beyond aim and spread", N.maxSpeed, N.maxDrift))
    Report(N.teamChecks > 0 and N.teamBad == 0 and N.greenChecks > 0 and N.greenBad == 0, "nano_colour_follows_TeamNanoSpray", "team colour", N.teamChecks, "checks", N.teamBad, "bad; nanoColor", N.greenChecks, "checks", N.greenBad, "bad", firstBad.teamBad or "")
    local open = 0
    for _ in pairs(nano.beams) do open = open + 1 end
    local mine, theirs = drawCells[1], drawCells[2]
    Report(open == 0, "nano_no_beam_left_open", "beams still open", open, "most particles alive at once", N.maxAlive)
    Report(mine and mine.beamFrames and mine.drawn > 0, "nano_drawn_for_own_repair", "particle draws", mine and mine.drawn, "beam frames", mine and mine.beamFrames, "in view", mine and mine.inView, "in los", mine and mine.los)
    Report(theirs and theirs.beamFrames and theirs.inView and not theirs.los and theirs.drawn == 0, "nano_hidden_outside_los", "particle draws", theirs and theirs.drawn, "beam frames", theirs and theirs.beamFrames, "in view", theirs and theirs.inView, "in los", theirs and theirs.los)
  end
  function gadget:Initialize()
    gadgetHandler:AddSyncAction("padprobe_click", Run)
    gadgetHandler:AddSyncAction("padprobe_frame", OnFrame)
    gadgetHandler:AddSyncAction("padprobe_end", OnEnd)
    gadgetHandler:AddSyncAction("padprobe_drawcell", OnDrawCell)
  end
  return
end

local SIZE = Game.mapSizeX
local LAKE_X0 = SIZE * 0.55
local TEAMS = { 0, 1, 2, 3, 4, 5 }

function gadget:Initialize()
  Spring.SetHeightMapFunc(function()
    for x = 0, SIZE, 8 do
      for z = 0, Game.mapSizeZ, 8 do
        if x > LAKE_X0 then Spring.SetHeightMap(x, z, -60) end
      end
    end
  end)
end

local solarDef, solarBuilt
function gadget:UnitCreated(uid, udid, team, builder) if udid == solarDef and builder then solarBuilt = uid end end

local vulnerable = {}
function gadget:UnitPreDamaged(uid)
  if not vulnerable[uid] then return 0, 0 end
end

local passes, fails = 0, 0
local function res(ok, name, ...)
  if ok then passes = passes + 1 else fails = fails + 1 end
  local t = { ... }
  for i = 1, #t do t[i] = tostring(t[i]) end
  Spring.Echo("[HARNESS] PAD " .. (ok and "PASS " or "FAIL ") .. name .. " " .. table.concat(t, " "))
end

local F = 0
local at, whens = {}, {}
local function After(frame, fn) local f = F + frame; at[f] = at[f] or {}; table.insert(at[f], fn) end
local function When(cond, fn, name) whens[#whens + 1] = { cond = cond, fn = fn, name = name, since = F } end

local function Spawn(name, x, z, team, built)
  local gy = Spring.GetGroundHeight(x, z)
  local u = Spring.CreateUnit(name, x, math.max(gy, 0), z, 0, team, built or false)
  if not u then res(false, "spawn", name) end
  return u
end

local function Hp(u) local h, m = Spring.GetUnitHealth(u); return h and h / m or -1 end
local function Hurt(u, f) local _, m = Spring.GetUnitHealth(u); Spring.SetUnitHealth(u, m * f) end
local function Trip(u) return GG.AirPads.trips[u] end
local function State(u) local t = Trip(u); return t and t.state or "-" end
local function Dist(u, x, z) local a, _, b = Spring.GetUnitPosition(u); return a and math.sqrt((a - x)^2 + (b - z)^2) or 1e9 end
local function Move(u, x, z, opts) Spring.GiveOrderToUnit(u, CMD.MOVE, { x, 100, z }, opts or 0) end
local function FirstCmd(u) return (Spring.GetUnitCurrentCommand(u)) end
local function Has(u, id)
  local q = Spring.GetUnitCommands(u, -1) or {}
  for i = 1, #q do if q[i].id == id then return true end end
  return false
end

-- planes followed every frame
local tracked = {}
local function Track(name, u)
  local p = { name = name, u = u, frames = {}, order = {}, last = "-", maxDeckOff = 0, maxDeckY = -1e9, minDeckY = 1e9, deckFrames = 0, maxDeckSpeed = 0 }
  tracked[#tracked + 1] = p
  return p
end
local function DeckCount(pad)
  local n = 0
  for _, pt in ipairs(GG.AirPads.pads[pad] and GG.AirPads.pads[pad].points or {}) do
    local t = pt.plane and Trip(pt.plane)
    if t and t.state == "deck" then n = n + 1 end
  end
  return n
end
local maxOnDeck = {}
local function StepTracked(frame)
  for _, p in ipairs(tracked) do
    if Spring.ValidUnitID(p.u) then
      local s = State(p.u)
      if s ~= p.last then
        p.order[#p.order + 1] = s
        p[s .. "At"] = p[s .. "At"] or frame
        Spring.Echo(string.format("[PADLOG] f=%d %s state %s -> %s hp=%.1f%%", frame, p.name, p.last, s, Hp(p.u) * 100))
        p.last = s
        if s == "-" then p.leftAt = frame; p.minAfter = 1e9 end
      end
      if p.leftAt and frame - p.leftAt < 75 then
        local x, y, z = Spring.GetUnitPosition(p.u)
        p.minAfter = math.min(p.minAfter, y - math.max(Spring.GetGroundHeight(x, z), 0))
      end
      p.frames[s] = (p.frames[s] or 0) + 1
      if s == "wait" then
        local wt = Trip(p.u)
        local x, y, z = Spring.GetUnitPosition(wt.waitPad)
        if x then
          local d = Dist(p.u, x, z)
          if d < 600 then p.joined = true end
          if p.joined then p.maxWait = math.max(p.maxWait or 0, d) end
        end
      end
      local t = Trip(p.u)
      local off, dy = -1, 0
      if t and t.point and t.pad then
        local px, py, pz = Spring.GetUnitPiecePosDir(t.pad.id, t.point.piece)
        local x, y, z = Spring.GetUnitPosition(p.u)
        off = math.sqrt((x - px)^2 + (z - pz)^2)
        dy = y - py
        if s == "deck" then
          p.deckFrames = p.deckFrames + 1
          p.maxDeckOff = math.max(p.maxDeckOff, off)
          p.maxDeckY = math.max(p.maxDeckY, dy)
          p.minDeckY = math.min(p.minDeckY, dy)
          local vx, vy, vz = Spring.GetUnitVelocity(t.pad.id)
          p.maxDeckSpeed = math.max(p.maxDeckSpeed, math.sqrt(vx * vx + vz * vz))
          p.pieceY = p.pieceY or select(2, Spring.GetUnitPiecePosition(p.u, 1))
          if not p.hp0 then p.hp0, p.hp0f = Hp(p.u), frame end
          p.hp1, p.hp1f = Hp(p.u), frame
          maxOnDeck[t.pad.id] = math.max(maxOnDeck[t.pad.id] or 0, DeckCount(t.pad.id))
        end
      end
      if frame % 30 == 0 then
        local x, y, z = Spring.GetUnitPosition(p.u)
        local vx, vy, vz = Spring.GetUnitVelocity(p.u)
        Spring.Echo(string.format("[PADLOG] f=%d %s hp=%.1f%% state=%s off=%.1f dy=%.1f y=%.1f ground=%.1f v=%.1f cmd=%s pos=%.0f,%.0f", frame, p.name, Hp(p.u) * 100, s, off, dy, y,
          math.max(Spring.GetGroundHeight(x, z), 0), math.sqrt(vx * vx + vy * vy + vz * vz), tostring((Spring.GetUnitCurrentCommand(p.u))), x, z))
      end
    end
  end
end

-- a Move on a plane ends well short of its goal (see the control in T.kinds): "got there" is the order finishing, closer than it began
local function OrderDone(u, id) local c = FirstCmd(u); return c ~= id end
local function Seq(p)
  return table.concat(p.order, ">")
end

-- a pad + plane cell; the plane is flying somewhere when it gets hurt
local function HurtWhileFlying(plane, _, _, tx, tz, hp, delay)
  Move(plane, tx, tz)
  After(delay or 150, function() Hurt(plane, hp or 0.2) end)
end

local T = {}
local START = 60

-- ------------------------------------------------------------- no pad, nanoframe pad, then finished pad (team 5)
function T.noPad()
  local x, z = 500, 9000
  local plane = Spawn("arm_t1_air_thunder", x, z, 5)
  local enemyPad = Spawn("arm_t2_def_airrepairpad", x + 600, z, 1)  -- another alliance's: must be ignored
  local p = Track("nopad", plane)
  Move(plane, x + 3000, z)
  After(100, function() Hurt(plane, 0.15) end)
  After(240, function()
    res(p.frames.fly == nil and State(plane) == "-" and FirstCmd(plane) == CMD.MOVE, "no_pad_keeps_order", "state", State(plane), "cmd", FirstCmd(plane), "hp", Hp(plane))
    -- a frame only
    local frame = Spawn("arm_t2_def_airrepairpad", x + 900, z + 500, 5, true)
    After(200, function()
      res(p.frames.fly == nil, "nanoframe_pad_ignored", "seq", Seq(p), "beingBuilt", Spring.GetUnitIsBeingBuilt(frame))
      local builder = Spawn("arm_t1_veh_constructor", x + 980, z + 500, 5)
      Spring.SetTeamResource(5, "es", 1e8); Spring.SetTeamResource(5, "e", 1e8); Spring.SetTeamResource(5, "ms", 1e8); Spring.SetTeamResource(5, "m", 1e8)
      Spring.GiveOrderToUnit(builder, CMD.REPAIR, { frame }, 0)
      Spring.SetUnitHealth(frame, { build = 0.999 })
      When(function() return not Spring.GetUnitIsBeingBuilt(frame) end, function()
        Spring.Echo("[PADLOG] nanoframe pad finished at f=" .. F)
        When(function() return Hp(plane) >= 1 and State(plane) == "-" end, function()
          res(p.deckFrames > 0, "finished_pad_used", "seq", Seq(p), "deck frames", p.deckFrames)
          -- last pad dies under the plane: back to its order with what health it has
          Move(plane, x + 2500, z - 1500)
          After(120, function()
            Hurt(plane, 0.15)
            When(function() return State(plane) == "deck" end, function()
              Spring.DestroyUnit(frame, false, true)
              local hpAt = Hp(plane)
              When(function() return State(plane) == "-" end, function()
                Spring.Echo("[PADLOG] nopad plane hp at kill " .. hpAt)
                When(function() return OrderDone(plane, CMD.MOVE) end, function()
                  res(Hp(plane) < 1 and not Has(plane, CMD_PAD), "last_pad_killed_back_to_order", "hp", string.format("%.2f", Hp(plane)), "seq", Seq(p), "dist to goal", string.format("%.0f", Dist(plane, x + 2500, z - 1500)))
                end, "last pad: reach order")
              end, "last pad: trip ends")
            end, "last pad: on deck")
          end)
        end, "finished pad: repaired")
      end, "pad finishes")
    end)
  end)
end

-- ------------------------------------------------------------- every kind: normal repair and resume
local KINDS = {
  { "fighter", "arm_t1_air_freedomfighter" }, { "bomber", "arm_t1_air_thunder" }, { "gunship", "arm_t2_air_brawler" }, { "transport", "arm_t1_air_atlas" },
  { "builder", "arm_t1_air_constructor" }, { "t2builder", "core_t2_air_advancedconstructor" }, { "seaplane", "core_t1_seapl_voodoo" }, { "corebomber", "core_t1_air_shadow" },
  { "scout", "core_t1_air_fink" }, { "t2gunship", "core_t2_air_rapier" }, { "t2fighter", "arm_t2_air_hawk" }, { "coretransport", "core_t1_air_valkyrie" },
}
function T.kinds()
  -- control: an unhurt plane on the same order, with the gadget not involved
  local ctl = Spawn("arm_t1_air_freedomfighter", 300, 7200, 2)
  Spring.GiveOrderToUnit(ctl, CMD.AUTOREPAIRLEVEL, { 0 }, 0)
  Spring.GiveOrderToUnit(ctl, CMD.FIRE_STATE, { 0 }, 0)
  Move(ctl, 2000, 7200)
  When(function() return F > START + 10 and OrderDone(ctl, CMD.MOVE) end, function()
    res(true, "control_move_ends_short_of_goal", "healthy fighter's Move ended", string.format("%.0f", Dist(ctl, 2000, 7200)), "elmos from goal")
  end, "control")
  for i, k in ipairs(KINDS) do
    local col, row = (i - 1) % 3, math.floor((i - 1) / 3)
    local x, z = 700 + col * 2000, 2000 + row * 1700
    local pad = Spawn(i % 2 == 1 and "arm_t2_def_airrepairpad" or "core_t2_def_airrepairpad", x, z, 1)
    local plane = Spawn(k[2], x - 500, z - 500, 1)
    Spring.GiveOrderToUnit(plane, CMD.FIRE_STATE, { 0 }, 0)
    local p = Track(k[1], plane)
    local tx, tz = x + 1700, z + 1000  -- far: a Move that starts within turn radius of its goal ends at once
    HurtWhileFlying(plane, x, z, tx, tz, 0.2, 90)
    When(function() return p.deckFrames > 0 and State(plane) == "-" end, function()
      local ud = UnitDefs[Spring.GetUnitDefID(plane)]
      local want = 800 / ud.buildTime * 100
      local got = p.hp1f > p.hp0f and (p.hp1 - p.hp0) * 100 / ((p.hp1f - p.hp0f) / 30) or 0
      local d0 = Dist(plane, tx, tz)
      local cmd0 = FirstCmd(plane)
      When(function() return OrderDone(plane, CMD.MOVE) end, function()
        res(cmd0 == CMD.MOVE and Dist(plane, tx, tz) < d0 and p.minAfter > 15 and Hp(plane) >= 1 and p.maxDeckY < 1 and p.minDeckY > -1 and math.abs(got - want) < want * 0.2, "normal_" .. k[1], "seq", Seq(p),
          string.format("deck dy %.2f..%.2f off %.2f deck %.1fs rate %.1f%%/s want %.1f hp %.0f%% after lift: cmd %s, min height %.0f, order ended %.0f from goal", p.minDeckY, p.maxDeckY, p.maxDeckOff, p.deckFrames / 30, got, want, Hp(plane) * 100,
            tostring(cmd0), p.minAfter or -1, Dist(plane, tx, tz)))
      end, "normal " .. k[1] .. ": back to move")
    end, "normal " .. k[1] .. ": repaired")
  end
end

-- ------------------------------------------------------------- every point busy (team 3: one pad, then a second one)
function T.busy()
  local x, z = 500, 7600
  local pad = Spawn("arm_t2_def_airrepairpad", x, z, 3)
  local list, ps = {}, {}
  local names = { "arm_t1_air_thunder", "arm_t1_air_freedomfighter", "arm_t2_air_brawler", "arm_t1_air_atlas" }
  for i = 1, 4 do
    local u = Spawn(names[i], x + 300 + i * 100, z + 200 * i, 3)
    list[i] = u
    ps[i] = Track("busy" .. i, u)
    Spring.GiveOrderToUnit(u, CMD.FIRE_STATE, { 0 }, 0)
    Move(u, x + 2500, z + 200 * i)
    After(120, function() Hurt(u, 0.2) end)
  end
  local maxOn = 0
  local function Sample()
    local on = 0
    for i = 1, 4 do
      local d = Dist(list[i], x, z)
      local y = select(2, Spring.GetUnitPosition(list[i]))
      if d < 5 and y < 125 then on = on + 1 end
    end
    maxOn = math.max(maxOn, on)
  end
  When(function()
    Sample()
    if F < START + 130 then return false end
    for i = 1, 4 do
      if Hp(list[i]) < 1 or State(list[i]) ~= "-" then return false end
    end
    return true
  end, function()
    local waited = 0
    local parts = {}
    for i = 1, 4 do
      waited = waited + ((ps[i].frames.wait or 0) > 0 and 1 or 0)
      parts[i] = Seq(ps[i]) .. string.format("(wait %.1fs, %.0f from pad at most)", (ps[i].frames.wait or 0) / 30, ps[i].maxWait or 0)
      if (ps[i].maxWait or 0) > 800 then maxOn = 99 end
    end
    res(maxOn <= 1 and waited >= 1 and Hp(list[1]) >= 1, "all_points_busy_one_pad", "planes down at once", maxOn, "waited", waited, table.concat(parts, " "))
    -- second pad: with the first full, the next plane takes the far one at once
    local far = Spawn("core_t2_def_airrepairpad", x + 1600, z, 3)
    After(5, function()
      for i = 1, 2 do Move(list[i], x + 2800, z + 1000 * i) end
      After(60, function()
        for i = 1, 2 do Hurt(list[i], 0.2); Track("busy2_" .. i, list[i]) end
      end)
    end)
    local n = #tracked
    After(70, function()
      local a, b = tracked[n + 1], tracked[n + 2]
      When(function() return a.deckFrames > 0 and b.deckFrames > 0 and State(list[1]) == "-" and State(list[2]) == "-" end, function()
        res((a.frames.wait or 0) == 0 and (b.frames.wait or 0) == 0, "other_pad_when_one_full", Seq(a), Seq(b))
      end, "busy: second pad used")
    end)
  end, "busy: all repaired")
end

-- ------------------------------------------------------------- carrier, standing: two points at once, third plane waits (team 4)
function T.carrierPoints()
  local x, z = LAKE_X0 + 3800, 2500
  local ship = Spawn("arm_t2_sea_colossus", x, z, 4)
  local us, ps = {}, {}
  for i = 1, 3 do
    us[i] = Spawn("arm_t1_air_thunder", x - 700, z - 400 + i * 150, 4)
    ps[i] = Track("deck" .. i, us[i])
    Spring.GiveOrderToUnit(us[i], CMD.FIRE_STATE, { 0 }, 0)
    Move(us[i], x + 1500, z - 400 + i * 150)
    After(120, function() Hurt(us[i], 0.2) end)
  end
  After(400, function() Spring.GiveOrderToUnit(ship, CMD.MOVE, { x, 0, z + 5000 }, 0) end)
  When(function() return F > START + 130 and Hp(us[1]) >= 1 and Hp(us[2]) >= 1 and Hp(us[3]) >= 1 and State(us[1]) == "-" and State(us[2]) == "-" and State(us[3]) == "-" end, function()
    res((maxOnDeck[ship] or 0) == 2, "carrier_two_points", "max on deck", maxOnDeck[ship], Seq(ps[1]), Seq(ps[2]), Seq(ps[3]), "waited s", (ps[1].frames.wait or 0) / 30, (ps[2].frames.wait or 0) / 30, (ps[3].frames.wait or 0) / 30, "max from ship", ps[1].maxWait or 0, ps[2].maxWait or 0, ps[3].maxWait or 0)
  end, "carrier points")
end

-- ------------------------------------------------------------- moving carrier
local function MovingShip(name, x, z, planeName, tag)
  local ship = Spawn(name, x, z, 1)
  local plane = Spawn(planeName, x - 700, z - 1100, 1)
  Spring.GiveOrderToUnit(plane, CMD.FIRE_STATE, { 0 }, 0)
  local goalX, goalZ = x - 4000 < LAKE_X0 + 200 and LAKE_X0 + 200 or x - 4000, z + 3200
  local p = Track(tag, plane)
  Spring.GiveOrderToUnit(ship, CMD.MOVE, { x + 1200, 0, goalZ }, 0)
  HurtWhileFlying(plane, x, z, x - 2000, z + 600, 0.2, 120)
  local y0
  When(function() return p.deckFrames > 0 end, function() y0 = F end, tag .. " down")
  When(function() return p.deckFrames > 0 and State(plane) == "-" end, function()
    res(p.maxDeckOff < 4 and p.maxDeckSpeed > 1 and Hp(plane) >= 1, "moving_" .. tag, "seq", Seq(p),
      string.format("max plane-point %.2f elmo, ship speed on deck up to %.2f e/f, dy %.2f..%.2f, deck %.1fs, hp %.0f%%", p.maxDeckOff, p.maxDeckSpeed, p.minDeckY, p.maxDeckY, p.deckFrames / 30, Hp(plane) * 100),
      "ship pos", Spring.GetUnitPosition(ship))
    local d0 = Dist(plane, x - 2000, z + 600)
    When(function() return OrderDone(plane, CMD.MOVE) end, function() res(Dist(plane, x - 2000, z + 600) < d0, "moving_" .. tag .. "_resumed", string.format("dist to goal %.0f -> %.0f", d0, Dist(plane, x - 2000, z + 600))) end, tag .. " resume")
  end, tag .. " repaired")
end
function T.moving()
  MovingShip("arm_t2_sea_colossus", LAKE_X0 + 1200, 500, "arm_t1_air_thunder", "colossus_bomber")
  MovingShip("core_t2_sea_hive", LAKE_X0 + 1200, 5500, "arm_t2_air_brawler", "hive_gunship")
  MovingShip("arm_t2_sea_colossus", LAKE_X0 + 3000, 8000, "arm_t1_air_atlas", "colossus_transport")
  MovingShip("core_t2_sea_hive", LAKE_X0 + 4000, 5500, "core_t1_air_avenger", "hive_fighter")
end

-- ------------------------------------------------------------- pad killed
function T.killed()
  local spots = { deck = { 3000, 7200 }, land = { 3000, 9800 }, fly = { 5000, 7200 } }
  for state, s in pairs(spots) do
    local x, z = s[1], s[2]
    local pad = Spawn("arm_t2_def_airrepairpad", x, z, 1)
    local other = Spawn("core_t2_def_airrepairpad", x + 600, z + 900, 1)
    local plane = Spawn("arm_t1_air_thunder", x - 600, z - 600, 1)
    Spring.GiveOrderToUnit(plane, CMD.FIRE_STATE, { 0 }, 0)
    local p = Track("killed_" .. state, plane)
    HurtWhileFlying(plane, x, z, x + 800, z - 800, 0.2, 120)
    When(function() return State(plane) == state and (state ~= "deck" or p.deckFrames > 30) end, function()
      Spring.DestroyUnit(pad, false, false)
      local hpAt = Hp(plane)
      When(function() return Hp(plane) >= 1 and State(plane) == "-" end, function()
        res(true, "pad_killed_in_" .. state, "seq", Seq(p), string.format("hp at kill %.0f%% end %.0f%%", hpAt * 100, Hp(plane) * 100), "other pad dist", string.format("%.0f", Dist(other, x, z)))
      end, "killed " .. state .. ": repaired elsewhere")
    end, "killed " .. state .. ": in state")
  end
end

-- ------------------------------------------------------------- the plane dies
function T.planeDies()
  local x, z = LAKE_X0 - 800, 10500
  local pad = Spawn("core_t2_def_airrepairpad", x, z, 4)
  local a = Spawn("arm_t1_air_thunder", x - 300, z - 300, 4)
  local b = Spawn("arm_t2_air_brawler", x + 300, z - 300, 4)
  local c = Spawn("arm_t1_air_freedomfighter", x - 300, z + 300, 4)
  local pa, pb, pc = Track("dies_deck", a), Track("dies_wait", b), Track("dies_after", c)
  for _, u in ipairs({ a, b, c }) do
    vulnerable[u] = true
    Spring.GiveOrderToUnit(u, CMD.FIRE_STATE, { 0 }, 0)
    Move(u, x + 1500, z + 1200)
  end
  After(90, function() Hurt(a, 0.2) end)
  When(function() return F > START + 90 and State(a) == "fly" end, function()
    Hurt(b, 0.2); Hurt(c, 0.2)
  end, "dies: a flies")
  local killedOnDeck = false
  When(function() return Spring.ValidUnitID(a) and State(a) == "deck" and pa.deckFrames > 15 end, function()
    Spring.AddUnitDamage(a, 1e6)
    killedOnDeck = true
    local waiter = State(b) == "wait" and b or c
    local other = waiter == b and c or b
    Spring.Echo("[PADLOG] plane killed on deck, b " .. State(b) .. " c " .. State(c))
    When(function() return Spring.ValidUnitID(c) and Hp(c) >= 1 and Spring.ValidUnitID(b) and Hp(b) >= 1 and State(b) == "-" and State(c) == "-" end, function()
      res(GG.AirPads.pads[pad].points[1].plane == nil and pb.deckFrames > 0 and pc.deckFrames > 0, "plane_killed_on_deck_frees_point", Seq(pb), Seq(pc))
      -- one dies while holding in the air
      Move(b, x + 1500, z + 1200); Move(c, x + 1500, z + 1200)
    end, "dies: others repaired")
  end, "dies: a on deck")
end

-- ------------------------------------------------------------- orders
function T.cancels()
  local function Cell(name, x, z, inState, order, check)
    Spawn("arm_t2_def_airrepairpad", x, z, 1)
    local plane = Spawn("arm_t1_air_thunder", x - 600, z - 600, 1)
    Spring.GiveOrderToUnit(plane, CMD.FIRE_STATE, { 0 }, 0)
    local p = Track("cancel_" .. name, plane)
    HurtWhileFlying(plane, x, z, x + 800, z - 800, 0.2, 120)
    When(function() return State(plane) == inState and (inState ~= "deck" or p.deckFrames > 15) end, function()
      local hpAt = Hp(plane)
      order(plane)
      check(plane, p, hpAt)
    end, "cancel " .. name .. ": in state")
  end
  local function MoveCheck(name, tx, tz)
    return function(plane, p, hpAt)
      local d0 = Dist(plane, tx, tz)
      When(function() return OrderDone(plane, CMD.MOVE) and State(plane) == "-" end, function()
        res(Hp(plane) < 0.99 and not Has(plane, CMD_PAD) and Dist(plane, tx, tz) < d0, "cancel_by_move_" .. name, "seq", Seq(p), string.format("hp %.0f%% dist to goal %.0f -> %.0f", Hp(plane) * 100, d0, Dist(plane, tx, tz)))
        -- the repair level comes back after a while
        When(function() return p.last ~= "-" end, function()
          res(true, "cancel_" .. name .. "_retries_later", "after", F, "frames")
        end, "cancel " .. name .. ": retry")
      end, "cancel " .. name .. ": reach")
    end
  end
  Cell("fly", 3000, 1200, "fly", function(u) Move(u, 4800, 1000) end, MoveCheck("fly", 4800, 1000))
  Cell("land", 5400, 1200, "land", function(u) Move(u, 6300, 2600) end, MoveCheck("land", 6300, 2600))
  Cell("deck", 3000, 11000, "deck", function(u) Move(u, 4400, 11300) end, MoveCheck("deck", 4400, 11300))
  Cell("stop", 5000, 11000, "deck", function(u) Spring.GiveOrderToUnit(u, CMD.STOP, {}, 0) end, function(plane, p, hpAt)
    When(function() return State(plane) == "-" end, function()
      res(not Has(plane, CMD_PAD), "cancel_by_stop_on_deck", "seq", Seq(p), "cmd", FirstCmd(plane))
      local x0, z0 = 5000, 11000
      After(100, function()
        local x, y, z = Spring.GetUnitPosition(plane)
        res(y - Spring.GetGroundHeight(x, z) < 5 and Dist(plane, x0, z0) > 60, "stop_on_deck_sets_down_off_the_pad", string.format("%.0f above ground, %.0f from pad", y - Spring.GetGroundHeight(x, z), Dist(plane, x0, z0)))
      end)
    end, "cancel stop")
  end)
end

-- ------------------------------------------------------------- repair level (team 2, allied to team 1: its nearest pad is team 1's)
function T.levels()
  local x, z = 500, 5400
  local pad = Spawn("arm_t2_def_airrepairpad", x, z - 1000, 1)
  local function Level(name, idx, hp, go)
    local plane = Spawn("arm_t1_air_thunder", x + idx * 400 + (go and 200 or 0), z + (go and 200 or 0), 2)
    Spring.GiveOrderToUnit(plane, CMD.FIRE_STATE, { 0 }, 0)
    local p = Track("level_" .. name, plane)
    After(5, function()
      if idx ~= 1 then Spring.GiveOrderToUnit(plane, CMD.AUTOREPAIRLEVEL, { idx }, 0) end
      Move(plane, x + idx * 400, z + 1200)
    end)
    After(120, function() Hurt(plane, hp) end)
    After(500, function()
      res(((p.frames.fly or 0) + (p.frames.wait or 0) > 0) == go, "level_" .. name .. "_hp" .. math.floor(hp * 100), "state", Spring.GetUnitStates(plane).autorepairlevel, "seq", Seq(p), "expected trip", go)
    end)
    return plane, p
  end
  local off, po = Level("off", 0, 0.05, false)
  Level("30", 1, 0.6, false)
  Level("30go", 1, 0.25, true)
  Level("50", 2, 0.4, true)
  Level("80", 3, 0.6, true)
  -- right click with the level off, and a healthy plane
  After(600, function()
    local given = Spring.GiveOrderToUnit(off, CMD_PAD, { pad }, 0)
    Spring.Echo("[PADLOG] manual order given " .. tostring(given) .. " cmd " .. tostring(FirstCmd(off)))
    When(function() return Hp(off) >= 1 and State(off) == "-" end, function()
      res(po.deckFrames > 0, "right_click_with_level_off_allied_pad", "seq", Seq(po), "pad team", Spring.GetUnitTeam(pad), "plane team", Spring.GetUnitTeam(off))
      local px, _, pz = Spring.GetUnitPosition(pad)
      After(300, function()
        local ax, ay, az = Spring.GetUnitPosition(off)
        res(ay - Spring.GetGroundHeight(ax, az) < 5 and FirstCmd(off) == nil and Dist(off, px, pz) > 60, "no_orders_after_repair_settles_off_the_pad", string.format("10 s after: %.0f above ground, %.0f from pad", ay - Spring.GetGroundHeight(ax, az), Dist(off, px, pz)))
      end)
    end, "manual")
    local healthy = Spawn("arm_t1_air_thunder", x + 2200, z, 2)
    After(30, function()
      Spring.GiveOrderToUnit(healthy, CMD_PAD, { pad }, 0)
      res(not Has(healthy, CMD_PAD), "right_click_rejected_at_full_health", "cmd", FirstCmd(healthy))
      Hurt(healthy, 0.95)
      Spring.GiveOrderToUnit(healthy, CMD_PAD, { 0 }, 0)
      res(not Has(healthy, CMD_PAD), "order_on_a_nonexistent_pad_rejected", "cmd", FirstCmd(healthy))
    end)
  end)
end

-- ------------------------------------------------------------- transfers
function T.transfer()
  local x, z = 500, 11000
  local pad = Spawn("arm_t2_def_airrepairpad", x, z, 1)
  local plane = Spawn("arm_t1_air_thunder", x - 400, z - 600, 1)
  Spring.GiveOrderToUnit(plane, CMD.FIRE_STATE, { 0 }, 0)
  local p = Track("transfer", plane)
  HurtWhileFlying(plane, x, z, x + 800, z - 800, 0.15, 120)
  -- to an ally on deck
  When(function() return State(plane) == "deck" and p.deckFrames > 15 end, function()
    Spring.TransferUnit(plane, 2, true)
    After(45, function()
      Spring.Echo("[PADLOG] transfer to ally: state " .. State(plane) .. " team " .. Spring.GetUnitTeam(plane) .. " cmd " .. tostring(FirstCmd(plane)))
      When(function() return State(plane) == "-" end, function()
        res(Spring.GetUnitTeam(plane) == 2, "transfer_to_ally_on_deck", "seq", Seq(p), string.format("hp %.0f%%", Hp(plane) * 100), "cmd", FirstCmd(plane))
        -- to an enemy on deck: it must leave. Team 2 is allied to 1, send it down again
        After(60, function()
          Hurt(plane, 0.15)
          Spring.GiveOrderToUnit(plane, CMD_PAD, { pad }, 0)
          local q = Track("transfer2", plane)
          When(function() return State(plane) == "deck" and q.deckFrames > 15 end, function()
            Spring.TransferUnit(plane, 3, true)
            When(function() return State(plane) == "-" end, function()
              local free = GG.AirPads.pads[pad].points[1].plane == nil
              res(Spring.GetUnitTeam(plane) == 3 and free, "transfer_to_enemy_on_deck", "seq", Seq(q), "point free", free, "hp", string.format("%.0f%%", Hp(plane) * 100))
              -- and the pad itself goes over to the enemy with a plane on it
              local pl2 = Spawn("arm_t1_air_thunder", x + 600, z + 400, 1)
              local r = Track("padgiven", pl2)
              Spring.GiveOrderToUnit(pl2, CMD.FIRE_STATE, { 0 }, 0)
              HurtWhileFlying(pl2, x, z, x + 1500, z - 300, 0.15, 90)
              When(function() return State(pl2) == "deck" and r.deckFrames > 15 end, function()
                Spring.TransferUnit(pad, 4, true)
                When(function() return r.last ~= "deck" and r.last ~= "lift" and r.frames.lift ~= nil end, function()
                  res(true, "pad_given_to_enemy_with_plane_on_it", "seq", Seq(r))
                end, "pad given")
              end, "pad given: deck")
            end, "transfer enemy: leaves")
          end, "transfer enemy: deck")
        end)
      end, "transfer ally: trip ends")
    end)
  end, "transfer: deck")
end

-- ------------------------------------------------------------- what they were doing
function T.resume()
  local function Cell(name, x, z, planeName, setup, check, hurtAt)
    local pad = Spawn("arm_t2_def_airrepairpad", x, z, 1)
    local plane = Spawn(planeName, x - 500, z - 300, 1)
    Spring.GiveOrderToUnit(plane, CMD.FIRE_STATE, { 0 }, 0)
    local p = Track("resume_" .. name, plane)
    setup(plane, x, z, p)
    After(hurtAt or 200, function() Hurt(plane, 0.2) end)
    When(function() return p.deckFrames > 0 and State(plane) == "-" end, function()
      check(plane, x, z, p)
    end, "resume " .. name)
  end
  -- ground attack: the order is still there
  Cell("attack", 7000 - 3000, 4500, "arm_t1_air_thunder", function(u, x, z)
    Spring.GiveOrderToUnit(u, CMD.ATTACK, { x + 900, 100, z + 900 }, 0)
  end, function(u, x, z, p) res(FirstCmd(u) == CMD.ATTACK, "resume_attack_order", "cmd", FirstCmd(u), "seq", Seq(p)) end)
  -- patrol on repeat: no trip command comes round again
  Cell("patrol", 6000, 3000, "arm_t2_air_brawler", function(u, x, z)
    Spring.GiveOrderToUnit(u, CMD.REPEAT, { 1 }, 0)
    Move(u, x + 700, z)
    Move(u, x + 700, z + 700, CMD.OPT_SHIFT)
    Move(u, x, z + 700, CMD.OPT_SHIFT)
  end, function(u, x, z, p)
    After(600, function()
      res(not Has(u, CMD_PAD) and #Spring.GetUnitCommands(u, -1) == 3, "resume_repeat_queue_keeps_3_moves", "queue", #Spring.GetUnitCommands(u, -1), "cmd", FirstCmd(u))
    end)
  end)
  -- builder halfway through a building
  Spring.SetTeamResource(1, "es", 1e8); Spring.SetTeamResource(1, "e", 1e8); Spring.SetTeamResource(1, "ms", 1e8); Spring.SetTeamResource(1, "m", 1e8)
  local solar = UnitDefNames.arm_t1_eco_solarcollector.id
  local built
  solarDef = solar
  Cell("build", 6000, 6000, "arm_t1_air_constructor", function(u, x, z, p)
    Spring.GiveOrderToUnit(u, -solar, { x + 400, 100, z + 300, 0 }, 0)
  end, function(u, x, z, p)
    When(function() return solarBuilt and not Spring.GetUnitIsBeingBuilt(solarBuilt) end, function()
      res(true, "resume_builder_finishes_building", "seq", Seq(p), "solar", solarBuilt)
    end, "builder finishes")
  end, 130)
  -- transport with cargo
  local cargo = Spawn("arm_t1_bot_peewee", 6000 + 200, 8000, 1)
  local t = Spawn("arm_t1_air_atlas", 6000 - 300, 8000, 1)
  local pad = Spawn("arm_t2_def_airrepairpad", 6000 - 1500, 8000, 1)
  local p = Track("resume_transport", t)
  Spring.GiveOrderToUnit(t, CMD.LOAD_UNITS, { cargo }, 0)
  Spring.GiveOrderToUnit(t, CMD.UNLOAD_UNITS, { 6000 - 900, 100, 8000 + 900, 100 }, CMD.OPT_SHIFT)
  When(function() local c = Spring.GetUnitIsTransporting(t); return c and c[1] end, function()
    Hurt(t, 0.2)
    When(function() return p.deckFrames > 0 end, function()
      local dy = select(2, Spring.GetUnitPosition(t)) - select(2, Spring.GetUnitPosition(pad))
      Spring.Echo("[PADLOG] transport with cargo on pad height above pad base " .. dy .. " cargo y " .. select(2, Spring.GetUnitPosition(cargo)))
    end, "transport down")
    When(function() return p.deckFrames > 0 and State(t) == "-" end, function()
      When(function() local c = Spring.GetUnitIsTransporting(t); return (not c or not c[1]) end, function()
        local x, y, z = Spring.GetUnitPosition(cargo)
        res(Hp(t) >= 1, "resume_transport_delivers_cargo", "seq", Seq(p), "cargo at", string.format("%.0f,%.0f", x, z), string.format("deck dy %.1f", p.maxDeckY))
      end, "transport unloads")
    end, "transport repaired")
  end, "transport loads")
  -- stunned pad: no repair while stunned
  local sp = Spawn("arm_t2_def_airrepairpad", 6000 - 1400, 1000, 1)
  local sa = Spawn("arm_t1_air_thunder", 6000 - 1900, 800, 1)
  Spring.GiveOrderToUnit(sa, CMD.FIRE_STATE, { 0 }, 0)
  local q = Track("stunpad", sa)
  HurtWhileFlying(sa, 0, 0, 6000 - 800, 500, 0.1, 100)
  When(function() return State(sa) == "deck" and q.deckFrames > 15 end, function()
    local _, m = Spring.GetUnitHealth(sp)
    Spring.SetUnitHealth(sp, { paralyze = m * 2 })
    local h0
    After(10, function() h0 = Hp(sa) end)
    After(70, function()
      res(Spring.GetUnitIsStunned(sp) and Hp(sa) == h0 and State(sa) == "deck", "stunned_pad_pauses_repair", "stunned", Spring.GetUnitIsStunned(sp), "hp", h0, Hp(sa))
      Spring.SetUnitHealth(sp, { paralyze = 0 })
      When(function() return Hp(sa) >= 1 and State(sa) == "-" end, function() res(true, "stunned_pad_recovers", "seq", Seq(q)) end, "stun recover")
    end)
  end, "stun: deck")
end

-- ------------------------------------------------------------- nano on screen: the player's pad, and an enemy's out of sight (the unsynced side watches)
function T.nanoView()
  for _, c in ipairs({ { 0, 1700, 11800, "mine" }, { 1, 1900, 10000, "theirs" } }) do
    local team, x, z = c[1], c[2], c[3]
    local pad = Spawn("arm_t2_def_airrepairpad", x, z, team)
    local plane = Spawn("arm_t1_air_thunder", x - 300, z, team)
    Spring.GiveOrderToUnit(plane, CMD.AUTOREPAIRLEVEL, { 0 }, 0)
    Spring.GiveOrderToUnit(plane, CMD.FIRE_STATE, { 0 }, 0)
    After(2, function()
      Hurt(plane, 0.2)
      Spring.GiveOrderToUnit(plane, CMD_PAD, { pad }, 0)
      SendToUnsynced("padprobe_drawcell", plane, pad, c[4])
    end)
  end
end

-- ------------------------------------------------------------- right click
function T.click()
  local x, z = 3500, 11700
  local plane = Spawn("arm_t1_air_thunder", x, z, 0)
  local full = Spawn("arm_t1_air_thunder", x + 100, z, 0)
  local pad = Spawn("arm_t2_def_airrepairpad", x + 400, z, 0)
  Hurt(plane, 0.5)
  Spring.GiveOrderToUnit(plane, CMD.AUTOREPAIRLEVEL, { 0 }, 0)
  After(3, function() SendToUnsynced("padprobe_click", plane, 0, pad, full) end)
end

-- -------------------------------------------------------------
local END = 7200
function gadget:GameFrame(frame)
  F = frame
  if frame == START - 5 then
    for _, t in ipairs(TEAMS) do
      Spring.SetTeamResource(t, "es", 1e8); Spring.SetTeamResource(t, "e", 1e8); Spring.SetTeamResource(t, "ms", 1e8); Spring.SetTeamResource(t, "m", 1e8)
    end
  end
  if frame == START then
    for _, n in ipairs({ "click", "nanoView", "kinds", "busy", "carrierPoints", "moving", "noPad", "planeDies", "killed", "cancels", "levels", "transfer", "resume" }) do T[n]() end
    -- the Land at button is what the UI sees
    local thunder = Spawn("arm_t1_air_thunder", 3000, 11700, 1)
    After(2, function()
      local i = Spring.FindUnitCmdDesc(thunder, CMD.AUTOREPAIRLEVEL)
      local d = Spring.GetUnitCmdDescs(thunder, i, i)[1]
      local j = Spring.FindUnitCmdDesc(thunder, CMD_PAD)
      local e = Spring.GetUnitCmdDescs(thunder, j, j)[1]
      res(d.type == CMDTYPE.ICON_MODE and #d.params == 5 and math.abs(Spring.GetUnitStates(thunder).autorepairlevel - 0.3) < 0.01 and e.hidden, "landat_button", "params", table.concat(d.params, "|"), "state", Spring.GetUnitStates(thunder).autorepairlevel, "type icon_mode", d.type == CMDTYPE.ICON_MODE, "pad desc hidden", e.hidden)
    end)
  end
  local list = at[frame]
  if list then
    at[frame] = nil
    for i = 1, #list do list[i]() end
  end
  local i = 1
  while whens[i] do
    local w = whens[i]
    if w.cond() then
      table.remove(whens, i)
      w.fn()
    else
      i = i + 1
    end
  end
  if frame > START then StepTracked(frame) end
  do -- who is being repaired right now, as this probe sees it: for the unsynced nano checks
    local parts = {}
    for unitID, trip in pairs(GG.AirPads.trips) do
      if trip.state == "deck" and trip.pad and Hp(unitID) < 1 and not Spring.GetUnitIsStunned(trip.pad.id) then
        parts[#parts + 1] = unitID .. ":" .. trip.pad.id
      end
    end
    SendToUnsynced("padprobe_frame", frame, table.concat(parts, ","))
  end
  if frame >= START + 60 and (frame % 300 == 0) then
    if #whens == 0 and next(at) == nil then END = frame end
  end
  if frame == END or frame == START + 7200 then
    for _, w in ipairs(whens) do res(false, "UNFINISHED", tostring(w.name), "waited", frame - w.since) end
    SendToUnsynced("padprobe_end")
    Spring.Echo("[HARNESS] PAD DONE pass " .. passes .. " fail " .. fails .. " at frame " .. frame)
    Spring.SendCommands("quitforce")
  end
end
