-- Pyro (CORE_T2_BOT_Pyro): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's CORE_T2_BOT_Pyro.COB: the torso turns at 180 deg/s and both arms pitch at 90 deg/s to aim; after
-- the restore delay (reload * 2) they return at 90 / 45 deg/s. Fires from firept, aims from the torso, SweetSpot =
-- torso, same death table and corpse types. The COB's PilotLight thread only flickered the 1998 flame polygons
-- (flame1..3, now empty flare pieces) and is dropped; the old walk is replaced by the shared one.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, ruparm, firept, luparm, lloarm = piece('ground', 'torso', 'ruparm', 'firept', 'luparm', 'lloarm')
flame1, flame2, flame3 = piece('flame1', 'flame2', 'flame3')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 4
local restoreDelay = 2000

function script.Create()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {torso})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(torso, y_axis, 0, rad(89.99))
	Turn(ruparm, x_axis, 0, rad(44.99))
	Turn(luparm, x_axis, 0, rad(44.99))
	WaitForTurn(torso, y_axis)
	WaitForTurn(ruparm, x_axis)
	WaitForTurn(luparm, x_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, rad(179.97))
	Turn(luparm, x_axis, -pitch, rad(89.98))
	Turn(ruparm, x_axis, -pitch, rad(89.98))
	WaitForTurn(torso, y_axis)
	WaitForTurn(luparm, x_axis)
	WaitForTurn(ruparm, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0
end

function script.QueryWeapon(num)
	return firept                 -- COB: piece 4
end

function script.FireWeapon(num)
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({firept, flame1, flame2, flame3, ground, lfoot, lleg, lloarm, lthigh, luparm, pelvis, rfoot, rleg, rthigh, ruparm, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({firept, flame1, flame2, flame3, ground, lfoot, lleg, lloarm, lthigh, luparm, pelvis, rfoot, rleg, rthigh}, SFX.FALL)
		Blow({ruparm}, SFX.SHATTER)
		Blow({torso}, SFX.NONE)
		return 2
	elseif severity <= 99 then
		Blow({firept, flame1, flame2, flame3, ground, lfoot, lleg, lloarm, lthigh, luparm, pelvis, rfoot, rleg, rthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({ruparm}, SFX.SHATTER)
		Blow({torso}, SFX.NONE)
		return 3
	end
	Blow({firept, flame1, flame2, flame3, ground, lfoot, lleg, lloarm, lthigh, luparm, pelvis, rfoot, rleg, rthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({ruparm}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	Blow({torso}, SFX.NONE)
	return 3
end
