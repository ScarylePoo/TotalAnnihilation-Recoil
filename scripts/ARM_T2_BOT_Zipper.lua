-- Zipper (ARM_T2_BOT_Zipper): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T2_BOT_Zipper.COB: to aim the torso turns at 250 deg/s, the cannon arm swings up level
-- (ruparm x -90 - pitch at 200 deg/s, forearm straight at 100 deg/s); each shot snaps the forearm to -50 deg as a kick;
-- after the restore delay (reload * 2) torso and arm return at 150 / 45 deg/s. Fires from rfirept, aims from the torso,
-- same death table and corpse types. The COB walk carried the cannon forward (rloarm about -80 deg) and the standing
-- pose let it hang into the ground; the shared walk (scripts/headers/walk.lua) does not move the arms, so the walk's
-- carry pose is the rest pose here.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, ruparm, rloarm, rfirept, luparm, lloarm, lhand =
	piece('ground', 'torso', 'ruparm', 'rloarm', 'rfirept', 'luparm', 'lloarm', 'lhand')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 4
local CARRY = rad(-80.16)         -- COB walk: rloarm x
local restoreDelay = 3000

function script.Create()
	Turn(rloarm, x_axis, CARRY)
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {torso})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(torso, y_axis, 0, rad(150))
	Turn(rloarm, x_axis, CARRY, rad(45))
	Turn(ruparm, x_axis, 0, rad(45))
	WaitForTurn(torso, y_axis)
	WaitForTurn(rloarm, x_axis)
	WaitForTurn(ruparm, x_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, rad(250))
	Turn(ruparm, x_axis, rad(-90) - pitch, rad(200))
	Turn(rloarm, x_axis, 0, rad(100))
	WaitForTurn(torso, y_axis)
	WaitForTurn(rloarm, x_axis)
	WaitForTurn(ruparm, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.FireWeapon(num)
	Turn(rloarm, x_axis, rad(-50))
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0
end

function script.QueryWeapon(num)
	return rfirept                -- COB: piece 1
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({ground, lhand, lloarm, lthigh, luparm, rfirept, rfoot, rleg, rthigh}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({ground}, SFX.NONE)
		Blow({lfoot, lleg, lthigh, pelvis, rfoot, rloarm, ruparm}, SFX.FALL)
		Blow({lhand, lloarm, luparm, rfirept, rleg, rthigh}, SFX.FALL + SFX.SMOKE)
		Blow({torso}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({ground, lfoot, lhand, lleg, lloarm, lthigh, luparm, pelvis, rfirept, rfoot, rleg, rloarm, rthigh, ruparm}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({torso}, SFX.SHATTER)
		return 2
	end
	Blow({ground, lfoot, lhand, lleg, lloarm, lthigh, luparm, pelvis, rfirept, rfoot, rleg, rloarm, rthigh, ruparm}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
