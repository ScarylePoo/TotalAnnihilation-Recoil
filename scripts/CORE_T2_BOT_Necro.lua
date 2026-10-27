-- Necro (CORE_T2_BOT_Necro): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's CORE_T2_BOT_Necro.COB: Activate/StartBuilding queue RequestState(0) -> Go (activatescr: the head
-- bows, both arms rise, the lathe tips forward and the claw opens, 100 ms keyframes; then the torso turns to the
-- build heading at 160 deg/s and INBUILDSTANCE is set); Deactivate/StopBuilding -> Stop (heading back,
-- deactivatescr). QueryNanoPiece = nanopoint, SweetSpot = torso; keyframes and the death table are the COB's, turn-z
-- values sign-flipped (Recoil CobInstance.h "COBWTF"). The old walk is replaced by the shared one.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
groundx2, torso, head, luparm, larm, finger1, finger2, thumb =
	piece('groundx2', 'torso', 'head', 'luparm', 'larm', 'finger1', 'finger2', 'thumb')
ruparm, rarm, lathe, nanopoint = piece('ruparm', 'rarm', 'lathe', 'nanopoint')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local buildHeading = 0

local function activatescr()
	Sleep(100)
	Move(head, y_axis, 1.25)
	Turn(luparm, x_axis, rad(13.68))
	Turn(ruparm, x_axis, rad(13.68))
	Turn(head, x_axis, rad(-15.5))
	Turn(rarm, x_axis, rad(-28.27))
	Turn(lathe, x_axis, rad(7.29))
	Turn(larm, x_axis, rad(-22.5))
	Turn(finger2, x_axis, rad(13.68))
	Turn(thumb, x_axis, rad(-12.46))
	Sleep(100)
	Move(head, y_axis, 1.5)
	Turn(luparm, x_axis, rad(27.36))
	Turn(ruparm, x_axis, rad(27.36))
	Turn(head, x_axis, rad(-31.01))
	Turn(rarm, x_axis, rad(-56.55))
	Turn(lathe, x_axis, rad(14.59))
	Turn(larm, x_axis, rad(-45))
	Turn(finger2, x_axis, rad(27.36))
	Turn(thumb, x_axis, rad(-24.93))
	Sleep(100)
	Move(head, y_axis, 1.375)
	Turn(luparm, x_axis, rad(7.29))
	Turn(ruparm, x_axis, rad(16.11))
	Turn(head, x_axis, rad(-33.75))
	Turn(rarm, x_axis, rad(-64.76))
	Turn(lathe, x_axis, rad(18.85))
	Sleep(100)
	Move(head, y_axis, 1.25)
	Turn(luparm, x_axis, rad(-12.77))
	Turn(ruparm, x_axis, rad(4.86))
	Turn(head, x_axis, rad(-36.49))
	Turn(rarm, x_axis, rad(-72.97))
	Turn(lathe, x_axis, rad(23.1))
	Sleep(100)
	Move(head, y_axis, 1.5)
	Turn(luparm, x_axis, rad(-31.92))
	Turn(ruparm, x_axis, rad(-15.2))
	Turn(rarm, x_axis, rad(-61.41))
	Turn(lathe, x_axis, rad(12.77))
	Turn(larm, x_axis, rad(-25.54))
	Sleep(100)
	Move(head, y_axis, 1.375)
	Turn(luparm, x_axis, rad(-51.08))
	Turn(ruparm, x_axis, rad(-35.27))
	Turn(rarm, x_axis, rad(-49.86))
	Turn(lathe, x_axis, rad(2.43))
	Turn(larm, x_axis, rad(-6.08))
	Sleep(100)
	Move(head, y_axis, 1)
	Turn(luparm, x_axis, rad(-69.02))
	Turn(ruparm, x_axis, rad(-52.9))
	Turn(rarm, x_axis, rad(-26.45))
	Turn(lathe, x_axis, rad(-5.47))
	Turn(larm, x_axis, rad(11.55))
	Turn(finger1, x_axis, rad(-8.82))
	Turn(finger2, x_axis, rad(12.46))
	Turn(thumb, y_axis, rad(0))
	Turn(thumb, z_axis, rad(-18.85))
	Sleep(100)
	Move(head, y_axis, 0.25)
	Turn(luparm, x_axis, rad(-86.96))
	Turn(ruparm, x_axis, rad(-70.54))
	Turn(rarm, x_axis, rad(-3.04))
	Turn(lathe, x_axis, rad(-13.38))
	Turn(larm, x_axis, rad(29.19))
	Turn(finger1, x_axis, rad(-17.63))
	Turn(finger2, x_axis, rad(-2.43))
	Turn(thumb, y_axis, rad(0))
	Turn(thumb, z_axis, rad(-37.7))
	Sleep(100)
	Move(head, y_axis, 0)
	Turn(luparm, x_axis, rad(-84.22))
	Turn(ruparm, x_axis, rad(-72.36))
	Turn(rarm, x_axis, rad(2.13))
	Turn(lathe, x_axis, rad(-19.15))
	Turn(larm, x_axis, rad(32.53))
	Turn(finger1, z_axis, rad(-12.16))
	Turn(finger2, z_axis, rad(10.03))
	Turn(thumb, z_axis, rad(-51.38))
	Sleep(100)
	Turn(luparm, x_axis, rad(-81.49))
	Turn(ruparm, x_axis, rad(-74.19))
	Turn(rarm, x_axis, rad(7.29))
	Turn(lathe, x_axis, rad(-24.93))
	Turn(larm, x_axis, rad(35.88))
	Turn(finger1, z_axis, rad(-24.32))
	Turn(finger2, z_axis, rad(20.07))
	Turn(thumb, z_axis, rad(-65.07))
	Sleep(100)
end

local function deactivatescr()
	Turn(luparm, x_axis, rad(-81.49))
	Turn(ruparm, x_axis, rad(-74.19))
	Turn(head, x_axis, rad(-36.49))
	Turn(rarm, x_axis, rad(7.29))
	Turn(lathe, x_axis, rad(-24.93))
	Turn(larm, x_axis, rad(35.88))
	Turn(finger1, x_axis, rad(-17.63))
	Turn(finger1, z_axis, rad(-24.32))
	Turn(finger2, x_axis, rad(-2.43))
	Turn(finger2, z_axis, rad(20.07))
	Turn(thumb, x_axis, rad(-24.93))
	Turn(thumb, y_axis, rad(0))
	Turn(thumb, z_axis, rad(-65.07))
	Sleep(100)
	Turn(luparm, x_axis, rad(-84.22))
	Turn(ruparm, x_axis, rad(-72.36))
	Turn(rarm, x_axis, rad(2.13))
	Turn(lathe, x_axis, rad(-19.15))
	Turn(larm, x_axis, rad(32.53))
	Turn(finger1, z_axis, rad(-12.16))
	Turn(finger2, z_axis, rad(10.03))
	Turn(thumb, z_axis, rad(-51.38))
	Sleep(100)
	Move(head, y_axis, 0.25)
	Turn(luparm, x_axis, rad(-86.96))
	Turn(ruparm, x_axis, rad(-70.54))
	Turn(rarm, x_axis, rad(-3.04))
	Turn(lathe, x_axis, rad(-13.38))
	Turn(larm, x_axis, rad(29.19))
	Turn(finger1, z_axis, rad(0))
	Turn(finger2, z_axis, rad(0))
	Turn(thumb, z_axis, rad(-37.7))
	Sleep(100)
	Move(head, y_axis, 1)
	Turn(luparm, x_axis, rad(-69.02))
	Turn(ruparm, x_axis, rad(-52.9))
	Turn(rarm, x_axis, rad(-26.45))
	Turn(lathe, x_axis, rad(-5.47))
	Turn(larm, x_axis, rad(11.55))
	Turn(finger1, x_axis, rad(-8.82))
	Turn(finger2, x_axis, rad(12.46))
	Turn(thumb, y_axis, rad(0))
	Turn(thumb, z_axis, rad(-18.85))
	Sleep(100)
	Move(head, y_axis, 1.375)
	Turn(luparm, x_axis, rad(-51.08))
	Turn(ruparm, x_axis, rad(-35.27))
	Turn(rarm, x_axis, rad(-49.86))
	Turn(lathe, x_axis, rad(2.43))
	Turn(larm, x_axis, rad(-6.08))
	Turn(finger1, x_axis, rad(0))
	Turn(finger2, x_axis, rad(27.36))
	Turn(thumb, y_axis, rad(0))
	Turn(thumb, z_axis, rad(0))
	Sleep(100)
	Move(head, y_axis, 1.5)
	Turn(luparm, x_axis, rad(-31.92))
	Turn(ruparm, x_axis, rad(-15.2))
	Turn(rarm, x_axis, rad(-61.41))
	Turn(lathe, x_axis, rad(12.77))
	Turn(larm, x_axis, rad(-25.54))
	Sleep(100)
	Move(head, y_axis, 1.25)
	Turn(luparm, x_axis, rad(-12.77))
	Turn(ruparm, x_axis, rad(4.86))
	Turn(rarm, x_axis, rad(-72.97))
	Turn(lathe, x_axis, rad(23.1))
	Turn(larm, x_axis, rad(-45))
	Sleep(100)
	Move(head, y_axis, 1.375)
	Turn(luparm, x_axis, rad(7.29))
	Turn(ruparm, x_axis, rad(16.11))
	Turn(head, x_axis, rad(-33.75))
	Turn(rarm, x_axis, rad(-64.76))
	Turn(lathe, x_axis, rad(18.85))
	Sleep(100)
	Move(head, y_axis, 1.5)
	Turn(luparm, x_axis, rad(27.36))
	Turn(ruparm, x_axis, rad(27.36))
	Turn(head, x_axis, rad(-31.01))
	Turn(rarm, x_axis, rad(-56.55))
	Turn(lathe, x_axis, rad(14.59))
	Sleep(100)
	Move(head, y_axis, 1.25)
	Turn(luparm, x_axis, rad(13.68))
	Turn(ruparm, x_axis, rad(13.68))
	Turn(head, x_axis, rad(-15.5))
	Turn(rarm, x_axis, rad(-28.27))
	Turn(lathe, x_axis, rad(7.29))
	Turn(larm, x_axis, rad(-22.5))
	Turn(finger2, x_axis, rad(13.68))
	Turn(thumb, x_axis, rad(-12.46))
	Sleep(100)
	Move(head, y_axis, 0)
	Turn(luparm, x_axis, rad(0))
	Turn(ruparm, x_axis, rad(0))
	Turn(head, x_axis, rad(0))
	Turn(rarm, x_axis, rad(0))
	Turn(lathe, x_axis, rad(0))
	Turn(larm, x_axis, rad(0))
	Turn(finger2, x_axis, rad(0))
	Turn(thumb, x_axis, rad(0))
	Sleep(100)
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
	return nanopoint              -- COB: piece 2
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 1
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({finger1, finger2, head, pelvis, larm, lathe, lfoot, lleg, luparm, rarm, rfoot, rleg, ruparm, thumb, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({finger1, finger2, head, pelvis, larm, lathe, lfoot, lleg, luparm, rarm, rfoot, rleg, ruparm, thumb}, SFX.FALL)
		Blow({torso}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({finger1, finger2, head, pelvis, larm, lathe, lfoot, lleg, luparm, rarm, rfoot, rleg, ruparm, thumb}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({torso}, SFX.SHATTER)
		return 3
	end
	Blow({finger1, finger2, head, pelvis, larm, lathe, lfoot, lleg, luparm, rarm, rfoot, rleg, ruparm, thumb}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
