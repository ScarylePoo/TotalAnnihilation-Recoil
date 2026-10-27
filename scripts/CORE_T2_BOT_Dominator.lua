-- Dominator (CORE_T2_BOT_Dominator): Lua unit script for the remodelled heavy rocket walker (standard biped skeleton).
-- Ported from TA's CORE_T2_BOT_Dominator.COB: AimPrimary yaws the head (150 deg/s) and tips the missile box (Launcher)
-- up to -90 deg about x (200 deg/s, vertical launch), RestoreAfterDelay brings both back (90 / 45 deg/s); the two
-- missile emit points (Missile1/Missile2, always hidden) alternate per shot; AimFrom = torso, SweetSpot = torso.
-- The COB's on/off missile slide (activatescr/deactivatescr) only moved the hidden missile pieces and is dropped; the
-- death table and corpse types are the COB's (old thigh1/leg1/foot1 = the right leg). The old walk is replaced by the
-- shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, head, launcher, missile1, missile2 = piece('ground', 'torso', 'head', 'launcher', 'missile1', 'missile2')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 2
local RESTORE_DELAY = 3000
local shot = 0

function script.Create()
	Hide(missile1)
	Hide(missile2)
	StartThread(SmokeUnit, {torso})
end

local function RestoreAfterDelay()
	Sleep(RESTORE_DELAY)
	Turn(head, y_axis, 0, rad(90))
	Turn(launcher, x_axis, 0, rad(45))
end

function script.AimFromWeapon(num)
	return torso
end

function script.QueryWeapon(num)
	if shot == 0 then return missile1 end
	return missile2
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(head, y_axis, heading, rad(150))
	Turn(launcher, x_axis, rad(-90), rad(200))
	WaitForTurn(head, y_axis)
	WaitForTurn(launcher, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.FireWeapon(num)
	shot = 1 - shot
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 2
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({rfoot, lfoot, ground, head, launcher, rleg, lleg, missile1, missile2, rthigh, lthigh, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({rfoot, lfoot, rleg, lleg, rthigh, lthigh}, SFX.FALL)
		Blow({ground, launcher}, SFX.NONE)
		Blow({head}, SFX.FALL + SFX.SMOKE)
		Blow({missile1, missile2}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({torso}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({rfoot, lfoot, rleg, lleg, rthigh, lthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({ground, launcher}, SFX.NONE)
		Blow({head, missile1, missile2}, SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({torso}, SFX.SHATTER)
		return 3
	end
	Blow({rfoot, lfoot, rleg, lleg, rthigh, lthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({ground, launcher}, SFX.NONE)
	Blow({head, missile1, missile2}, SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
