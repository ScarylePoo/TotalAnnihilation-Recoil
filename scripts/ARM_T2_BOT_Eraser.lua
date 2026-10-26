-- Eraser (ARM_T2_BOT_Eraser): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T2_BOT_Eraser.COB: Activate drops the two jammer tongs and their mount out of the beam
-- (7.5 elmo at ~10 elmo/s), swings the tongs forward (ltong -119.17 / rtong +116.72 deg about y) and spins the hub
-- (tongpivot) about z at 100 deg/s; Deactivate turns the hub back to 0, swings the tongs in and raises them again.
-- Timings, SweetSpot (torso) and the death table are the COB's. COB negates spin/turn values on the z axis (Recoil
-- CobInstance.h "COBWTF"), so the hub spin is sign-flipped here; the COB's zero-speed turns are no-ops and dropped.
-- The old walk is replaced by the shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, tongpivot, ltong, rtong, tongend = piece('ground', 'torso', 'tongpivot', 'ltong', 'rtong', 'tongend')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_ACT = 2

local function Open()
	Move(tongend, y_axis, 0); Move(ltong, y_axis, 0); Move(rtong, y_axis, 0)
	Move(tongend, y_axis, -7.5, 9.987); Move(ltong, y_axis, -7.5, 9.987); Move(rtong, y_axis, -7.5, 9.987)
	Sleep(751)
	Turn(ltong, y_axis, rad(-119.17), rad(157.23))
	Turn(rtong, y_axis, rad(116.72), rad(153.98))
	Sleep(775)
end

local function Close()
	Move(tongend, y_axis, -7.5); Move(ltong, y_axis, -7.5); Move(rtong, y_axis, -7.5)
	Turn(ltong, y_axis, rad(-119.17)); Turn(rtong, y_axis, rad(116.72))
	Turn(ltong, y_axis, 0, rad(174.51))
	Turn(rtong, y_axis, 0, rad(170.94))
	Sleep(683)
	Move(tongend, y_axis, 0, 10.885); Move(ltong, y_axis, 0, 10.885); Move(rtong, y_axis, 0, 10.885)
	Sleep(710)
end

function script.Create()
	StartThread(SmokeUnit, {torso})
end

local function ActivateThread()
	Signal(SIG_ACT)
	SetSignalMask(SIG_ACT)
	Open()
	Spin(tongpivot, z_axis, rad(-100))
end

local function DeactivateThread()
	Signal(SIG_ACT)
	SetSignalMask(SIG_ACT)
	Turn(tongpivot, z_axis, 0, rad(100))
	WaitForTurn(tongpivot, z_axis)
	Close()
end

function script.Activate()
	StartThread(ActivateThread)
end

function script.Deactivate()
	StartThread(DeactivateThread)
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({lfoot, lleg, lthigh, ltong, pelvis, rfoot, rleg, rthigh, rtong, tongend, tongpivot, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({lfoot, lleg, pelvis, rfoot, rleg, rtong, tongend, tongpivot}, SFX.FALL)
		Blow({lthigh, rthigh, torso}, SFX.NONE)
		Blow({ltong}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({lfoot, lleg, pelvis, rfoot, rleg, rtong, tongend, tongpivot}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({lthigh, rthigh, torso}, SFX.NONE)
		Blow({ltong}, SFX.SHATTER)
		return 3
	end
	Blow({lfoot, lleg, pelvis, rfoot, rleg, rtong, tongend, tongpivot}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({lthigh, rthigh, torso}, SFX.NONE)
	Blow({ltong}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
