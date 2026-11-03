-- Spectre (CORE_T2_BOT_Spectre): Lua unit script for the remodelled jammer walker (standard biped skeleton).
-- Ported from TA's CORE_T2_BOT_Spectre.COB: Activate flips both jammer tongs forward (x 180 deg at 317 deg/s) and
-- spins the hub (tongspivot) about z at 100 deg/s; Deactivate turns the hub back to 0 and folds the tongs (180 deg/s).
-- SweetSpot = torso; the death table and corpse types are the COB's. COB spin/turn values on z are sign-flipped
-- (Recoil CobInstance.h "COBWTF"). The old walk (which also swayed the skirt) is replaced by the shared one.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, legcover, tongspivot, ltong, rtong = piece('ground', 'torso', 'legcover', 'tongspivot', 'ltong', 'rtong')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_ACT = 2

local function open()
	Move(torso, y_axis, -1.25)
	Turn(ltong, x_axis, rad(0))
	Turn(ltong, x_axis, rad(180), rad(316.9))
	Turn(rtong, x_axis, rad(0))
	Turn(rtong, x_axis, rad(180), rad(316.9))
	Sleep(568)
	Sleep(8)
end

local function close()
	Move(torso, y_axis, -1.25)
	Turn(ltong, x_axis, rad(179.65))
	Turn(ltong, x_axis, rad(0), rad(180.01))
	Turn(rtong, x_axis, rad(180))
	Turn(rtong, x_axis, rad(0), rad(180.36))
	Sleep(998)
	Sleep(8)
end
local function ActivateThread()
	Signal(SIG_ACT)
	SetSignalMask(SIG_ACT)
	open()
	Spin(tongspivot, z_axis, rad(-100))
end

local function DeactivateThread()
	Signal(SIG_ACT)
	SetSignalMask(SIG_ACT)
	Turn(tongspivot, z_axis, 0, rad(100))
	WaitForTurn(tongspivot, z_axis)
	close()
end

function script.Create()
	Move(torso, y_axis, -1.25)      -- the kit model's torso sat 1.15 above the pelvis at rest
	StartThread(SmokeUnit, {torso})
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
		Blow({ground, legcover, lfoot, lleg, lthigh, ltong, pelvis, rfoot, rleg, rthigh, rtong, tongspivot, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({ground, lfoot, lleg, lthigh, ltong, pelvis, rfoot, rleg, rthigh, rtong, tongspivot, torso}, SFX.FALL)
		Blow({legcover}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({ground, lfoot, lleg, lthigh, ltong, pelvis, rfoot, rleg, rthigh, rtong, tongspivot, torso}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({legcover}, SFX.SHATTER)
		return 3
	end
	Blow({ground, lfoot, lleg, lthigh, ltong, pelvis, rfoot, rleg, rthigh, rtong, tongspivot, torso}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({legcover}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
