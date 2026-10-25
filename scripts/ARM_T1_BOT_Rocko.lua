-- Rocko (ARM_T1_BOT_Rocko): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T1_BOT_Rocko.COB: torso 130 deg/s, the rocket pod swings 90 deg forward at 95 deg/s to aim
-- and back at 45 deg/s after the restore delay, the launch tube kicks 3.75 elmo into the pod, rockets leave from
-- lbarrel; same death table and corpse types. The COB's MotionControl also re-centred torso/pod when standing still
-- and not aiming; RestoreAfterDelay already does that, so it went with the old walk.
-- The walk is the shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, lmisspod, lbarrel, lfirept2, rshield = piece('ground', 'torso', 'lmisspod', 'lbarrel', 'lfirept2', 'rshield')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 4
local restoreDelay = 3000

function script.Create()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {torso, pelvis})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(torso, y_axis, 0, rad(90))
	Turn(lmisspod, x_axis, 0, rad(45))
	WaitForTurn(torso, y_axis)
	WaitForTurn(lmisspod, x_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, rad(130))
	Turn(lmisspod, x_axis, rad(-90), rad(95))
	WaitForTurn(torso, y_axis)
	WaitForTurn(lmisspod, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0
end

function script.QueryWeapon(num)
	return lbarrel                -- COB: piece 1
end

function script.FireWeapon(num)
	Move(lbarrel, y_axis, 3.75, 62.5)
	WaitForMove(lbarrel, y_axis)
	Move(lbarrel, y_axis, 0, 1.875)
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local DEATH = {ground, lbarrel, lfirept2, lfoot, lleg, lmisspod, lthigh, pelvis, rfoot, rleg, rshield, rthigh}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.NONE) end
		Explode(torso, SFX.NONE)
		return 1
	elseif severity <= 50 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.FALL) end
		Explode(torso, SFX.SHATTER)
		return 2
	end
	local f = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	for _, p in ipairs(DEATH) do Explode(p, f) end
	Explode(torso, SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0))
	return 3
end
