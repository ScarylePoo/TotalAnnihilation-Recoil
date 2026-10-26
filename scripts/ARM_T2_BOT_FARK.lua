-- FARK (ARM_T2_BOT_FARK): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T2_BOT_FARK.COB: Activate/StartBuilding queue RequestState(0) -> Go (activatescr: arms raised
-- and spread, lathes angled in, torso leans 28 deg forward; then the torso turns to the build heading at 160 deg/s and
-- INBUILDSTANCE is set); Deactivate/StopBuilding -> Stop (heading back, deactivatescr). Speeds, sleeps, SweetSpot
-- (torso) and the death table are the COB's; turn-z values are sign-flipped (Recoil CobInstance.h "COBWTF").
-- QueryNanoPiece alternates the two arms like the COB, but emits from the lathe tips (llathepoint/rlathepoint) instead
-- of the lathe pivots so the spray leaves the cyan emitters. The old walk is replaced by the shared one.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
groundx2, torso, head, shield1, shield2, shield3, shield4 =
	piece('groundx2', 'torso', 'head', 'shield1', 'shield2', 'shield3', 'shield4')
lshoulder, larm, llathe, llathepoint = piece('lshoulder', 'larm', 'llathe', 'llathepoint')
rshoulder, rarm, rlathe, rlathepoint = piece('rshoulder', 'rarm', 'rlathe', 'rlathepoint')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local buildHeading = 0
local nano = 0

local function activatescr()
	Turn(lshoulder, x_axis, rad(0))
	Turn(lshoulder, x_axis, rad(-10.94), rad(59.17))
	Turn(rshoulder, x_axis, rad(0))
	Turn(rshoulder, x_axis, rad(-10.64), rad(57.52))
	Turn(rarm, x_axis, rad(0))
	Turn(rarm, x_axis, rad(-22.19), rad(119.98))
	Turn(larm, x_axis, rad(0))
	Turn(larm, x_axis, rad(-22.19), rad(119.98))
	Sleep(185)
	Turn(lshoulder, x_axis, rad(-21.89), rad(48.65))
	Turn(rshoulder, x_axis, rad(-21.28), rad(47.3))
	Turn(rarm, x_axis, rad(-44.39), rad(98.65))
	Turn(larm, x_axis, rad(-44.39), rad(98.65))
	Sleep(225)
	Turn(rarm, z_axis, rad(-33.44), rad(145.42))
	Turn(rlathe, z_axis, rad(63.85), rad(277.61))
	Turn(larm, z_axis, rad(33.44), rad(145.42))
	Turn(llathe, z_axis, rad(-62.63), rad(272.32))
	Sleep(230)
	Turn(torso, x_axis, rad(27.97), rad(121.62))
	Turn(rarm, z_axis, rad(-20.07), rad(58.16))
	Turn(larm, z_axis, rad(20.07), rad(58.16))
	Sleep(230)
	Sleep(10)
end

local function deactivatescr()
	Turn(torso, x_axis, rad(27.97))
	Turn(torso, x_axis, rad(0), rad(139.86))
	Turn(lshoulder, x_axis, rad(-21.89))
	Turn(rshoulder, x_axis, rad(-21.28))
	Turn(rarm, x_axis, rad(-44.39))
	Turn(rarm, z_axis, rad(-20.07))
	Turn(rarm, z_axis, rad(-33.44), rad(66.89))
	Turn(rlathe, z_axis, rad(63.85))
	Turn(larm, x_axis, rad(-44.39))
	Turn(larm, z_axis, rad(20.07))
	Turn(larm, z_axis, rad(33.44), rad(66.89))
	Turn(llathe, z_axis, rad(-62.63))
	Sleep(200)
	Turn(rarm, z_axis, rad(0), rad(167.23))
	Turn(rlathe, z_axis, rad(0), rad(319.25))
	Turn(larm, z_axis, rad(0), rad(167.23))
	Turn(llathe, z_axis, rad(0), rad(313.17))
	Sleep(200)
	Turn(lshoulder, x_axis, rad(-10.94), rad(54.73))
	Turn(rshoulder, x_axis, rad(-10.64), rad(53.21))
	Turn(rarm, x_axis, rad(-22.19), rad(110.98))
	Turn(larm, x_axis, rad(-22.19), rad(110.98))
	Sleep(200)
	Turn(lshoulder, x_axis, rad(0), rad(54.73))
	Turn(rshoulder, x_axis, rad(0), rad(53.21))
	Turn(rarm, x_axis, rad(0), rad(110.98))
	Turn(larm, x_axis, rad(0), rad(110.98))
	Sleep(200)
	Sleep(10)
end
local function Go()
	activatescr()
	Turn(torso, y_axis, buildHeading, rad(160))
	WaitForTurn(torso, y_axis)
	SetUnitValue(COB.INBUILDSTANCE, 1)
end

local function Stop()
	SetUnitValue(COB.INBUILDSTANCE, 0)
	Turn(torso, y_axis, 0, rad(160))
	WaitForTurn(torso, y_axis)
	deactivatescr()
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
	StartThread(SmokeUnit, {torso})
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
	nano = 1 - nano
	return (nano == 1) and llathepoint or rlathepoint
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 2
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({head, pelvis, larm, lfoot, llathe, llathepoint, lleg, lshoulder, rarm, rfoot, rlathe, rlathepoint, rleg, rshoulder, shield1, shield2, shield3, shield4, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({head}, SFX.SHATTER)
		Blow({pelvis, larm, lfoot, llathe, llathepoint, lleg, lshoulder, rarm, rfoot, rlathe, rlathepoint, rleg, rshoulder}, SFX.FALL)
		Blow({shield1, shield2, shield3, shield4, torso}, SFX.NONE)
		return 2
	elseif severity <= 99 then
		Blow({head}, SFX.SHATTER)
		Blow({pelvis, larm, lfoot, llathe, llathepoint, lleg, lshoulder, rarm, rfoot, rlathe, rlathepoint, rleg, rshoulder}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({shield1, shield2, shield3, shield4, torso}, SFX.NONE)
		return 3
	end
	Blow({head}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	Blow({pelvis, larm, lfoot, llathe, llathepoint, lleg, lshoulder, rarm, rfoot, rlathe, rlathepoint, rleg, rshoulder}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({shield1, shield2, shield3, shield4, torso}, SFX.NONE)
	return 3
end
