-- Advanced Construction Kbot (ARM_T2_BOT_AdvancedConstructor): Lua unit script for the remodelled walker (standard
-- biped skeleton). Ported from TA's ARM_T2_BOT_AdvancedConstructor.COB: Activate/StartBuilding queue RequestState(0)
-- -> Go (open: the roof swings up -68 deg, the frame lifts and flips the emitters out; then the torso turns to the
-- build heading at 160 deg/s and INBUILDSTANCE is set); Deactivate/StopBuilding -> Stop (heading back, close).
-- QueryNanoPiece alternates rnanospray/lnanospray, SweetSpot = torso; speeds, sleeps and the death table are the
-- COB's. The COB's leg resets inside open/close belong to the old walk and are dropped (the shared walk owns the legs).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, guncase, nanoarm, nanojoint = piece('ground', 'torso', 'guncase', 'nanoarm', 'nanojoint')
lnanogun, lnanospray, rnanogun, rnanospray = piece('lnanogun', 'lnanospray', 'rnanogun', 'rnanospray')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local buildHeading = 0
local nano = 0

local function open()
	Turn(guncase, x_axis, rad(0))
	Turn(guncase, x_axis, rad(-68.1), rad(90.81))
	Turn(nanojoint, x_axis, rad(0))
	Turn(nanojoint, x_axis, rad(-4.22), rad(5.62))
	Sleep(750)
	Turn(nanoarm, x_axis, rad(-52.73), rad(69.57))
	Turn(nanojoint, x_axis, rad(43.94), rad(63.54))
	Sleep(758)
	Turn(nanoarm, x_axis, rad(-87.54), rad(45.91))
	Turn(nanojoint, x_axis, rad(157.5), rad(149.8))
	Sleep(758)
	Sleep(30)
end

local function close()
	Turn(guncase, x_axis, rad(-68.1))
	Turn(nanoarm, x_axis, rad(-87.54))
	Turn(nanoarm, x_axis, rad(0), rad(116.56))
	Turn(nanojoint, x_axis, rad(157.5))
	Turn(nanojoint, x_axis, rad(0), rad(209.72))
	Sleep(751)
	Turn(guncase, x_axis, rad(0.09), rad(89.97))
	Sleep(758)
	Sleep(40)
end
local function Go()
	open()
	Turn(torso, y_axis, buildHeading, rad(160))
	WaitForTurn(torso, y_axis)
	SetUnitValue(COB.INBUILDSTANCE, 1)
end

local function Stop()
	SetUnitValue(COB.INBUILDSTANCE, 0)
	Turn(torso, y_axis, 0, rad(160))
	WaitForTurn(torso, y_axis)
	close()
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
	local p = (nano == 0) and rnanospray or lnanospray   -- COB: pieces 0 / 1
	nano = 1 - nano
	return p
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 2
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({ground, guncase, lfoot, lleg, lnanogun, lnanospray, lthigh, nanoarm, nanojoint, pelvis, rfoot, rleg, rnanogun, rnanospray, rthigh, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({ground, guncase, lfoot, lnanogun, lthigh, nanoarm, pelvis, rfoot, rnanogun, rthigh, torso}, SFX.NONE)
		Blow({lleg, lnanospray, rleg, rnanospray}, SFX.FALL)
		Blow({nanojoint}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({ground, guncase, lnanogun, pelvis, rnanogun, torso}, SFX.NONE)
		Blow({lfoot, lleg, lnanospray, lthigh, rfoot, rleg, rnanospray, rthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({nanoarm, nanojoint}, SFX.SHATTER)
		return 3
	end
	Blow({ground, guncase, lnanogun, pelvis, rnanogun, torso}, SFX.NONE)
	Blow({lfoot, lleg, lnanospray, lthigh, rfoot, rleg, rnanospray, rthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({nanoarm, nanojoint}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
