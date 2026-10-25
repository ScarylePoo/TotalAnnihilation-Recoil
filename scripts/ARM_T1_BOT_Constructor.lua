-- Construction Kbot (ARM_T1_BOT_Constructor): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T1_BOT_Constructor.COB: Go folds the roof panels out (97 deg at 350 deg/s), swings the front
-- hatch up 126 deg, raises the nano gun (arms +90 / nanobody2 -90), telescopes the nozzle 11 elmo and turns the turret
-- to the build heading at 300 deg/s before setting INBUILDSTANCE; Stop clears it and runs the COB's close sequence.
-- Same RequestState queue (StartBuilding/Activate -> open, StopBuilding/Deactivate -> close), QueryNanoPiece =
-- nanospray, SweetSpot = turret, same death table and corpse types. COB negates turn-z destinations (Recoil
-- CobInstance.h "COBWTF"), so the roof-panel angles are sign-flipped here. The COB's zero-speed "hold" turns are
-- no-ops at their destination and are left out. The walk is the shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, turret, lflap, rflap, arms, nanobody2, nozzle, nanospray, guncover =
	piece('ground', 'turret', 'lflap', 'rflap', 'arms', 'nanobody2', 'nozzle', 'nanospray', 'guncover')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SPD = rad(349.91)
local buildHeading = 0

local function Go()
	Turn(lflap, z_axis, 0); Turn(lflap, z_axis, rad(-96.99), SPD)
	Turn(rflap, z_axis, 0); Turn(rflap, z_axis, rad(96.99), SPD)
	Sleep(300)
	Turn(guncover, x_axis, rad(126), SPD)
	Sleep(300)
	Turn(arms, x_axis, rad(89.99), SPD)
	Turn(nanobody2, x_axis, rad(-89.99), SPD)
	Sleep(100)
	Move(nozzle, z_axis, 11, 45)
	Sleep(150)
	Turn(turret, y_axis, buildHeading, rad(299.93))
	WaitForTurn(turret, y_axis)
	SetUnitValue(COB.INBUILDSTANCE, 1)
end

local function Stop()
	SetUnitValue(COB.INBUILDSTANCE, 0)
	Turn(turret, y_axis, 0, SPD)
	WaitForTurn(turret, y_axis)
	Move(nozzle, z_axis, 11)
	Move(nozzle, z_axis, -0.5, 45)
	Turn(guncover, x_axis, rad(126.89))
	Turn(lflap, z_axis, rad(-97.9))
	Turn(rflap, z_axis, rad(97.9))
	Turn(arms, x_axis, rad(89.99))
	Turn(nanobody2, x_axis, rad(-89.99))
	Sleep(50)
	Turn(arms, x_axis, 0, SPD)
	Turn(nanobody2, x_axis, rad(-40), SPD)
	Sleep(50)
	Turn(nanobody2, x_axis, 0, SPD)
	Sleep(50)
	Turn(guncover, x_axis, 0, SPD)
	Sleep(50)
	Turn(lflap, z_axis, 0, SPD)
	Turn(rflap, z_axis, 0, SPD)
	Sleep(100)
end

-- COB RequestState: one worker runs Go/Stop until the requested state stops changing (0 = open, 1 = closed)
local wanted, current, busy = 1, 1, false
local function RequestState(state)
	wanted = state
	if busy then return end
	busy = true
	while wanted ~= current do
		current = wanted
		if current == 0 then Go() else Stop() end
	end
	busy = false
end

function script.Create()
	StartThread(SmokeUnit, {pelvis, turret})
end

function script.Activate()
	StartThread(RequestState, 0)
end

function script.Deactivate()
	StartThread(RequestState, 1)
end

function script.StartBuilding(heading, pitch)
	buildHeading = heading
	StartThread(RequestState, 0)
end

function script.StopBuilding()
	StartThread(RequestState, 1)
end

function script.QueryNanoPiece()
	return nanospray              -- COB: piece 0
end

function script.SweetSpot(num)
	return turret                 -- COB: piece 1
end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	for _, p in ipairs({ground, lflap, nanobody2, pelvis, rflap, turret}) do Explode(p, SFX.NONE) end
	if severity <= 25 then
		for _, p in ipairs({arms, guncover, lfoot, nanospray, nozzle, rfoot}) do Explode(p, SFX.NONE) end
		return 1
	elseif severity <= 50 then
		for _, p in ipairs({arms, guncover, nanospray, nozzle}) do Explode(p, SFX.FALL) end
		Explode(lfoot, SFX.SHATTER); Explode(rfoot, SFX.SHATTER)
		return 2
	end
	local f = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	for _, p in ipairs({arms, guncover, nanospray, nozzle}) do Explode(p, f) end
	local s = SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0)
	Explode(lfoot, s); Explode(rfoot, s)
	return 3
end
