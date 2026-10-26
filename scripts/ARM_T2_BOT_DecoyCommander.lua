-- Decoy Commander (ARM_T2_BOT_DecoyCommander): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T2_BOT_DecoyCommander.COB: the laser (weapon 1) turns the torso at 300 deg/s and raises the
-- left (lathe/laser) arm to -pitch - 30 deg at 90 deg/s, fires from lfirept; a third weapon slot (the D-gun in the
-- real commander's script) raises the right arm to -pitch - 24 deg and fires from rbigflash, and while it is aimed the
-- laser does not aim. Building aims the lathe arm the same way and sets INBUILDSTANCE; nano spray from nanospray.
-- RestorePosition (torso 90 deg/s, arms 45 deg/s) ran on the COB-only TargetCleared callin; here it runs after a
-- restore delay (reload * 2) and on StopBuilding. The COB has no Killed: the wreck is always left (corpse 1).
-- The old walk is replaced by the shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, head, ruparm, biggun, rbigflash = piece('ground', 'torso', 'head', 'ruparm', 'biggun', 'rbigflash')
luparm, nanolath, lfirept, nanospray = piece('luparm', 'nanolath', 'lfirept', 'nanospray')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 2
local restoreDelay = 3000
local bigGunAimed = false     -- COB static 3

function script.Create()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = math.max(1000, WeaponDefs[wd.weaponDef].reload * 2000)
	end
	StartThread(SmokeUnit, {torso})
end

local function RestorePosition()
	bigGunAimed = false
	Turn(torso, y_axis, 0, rad(89.98))
	Turn(ruparm, x_axis, 0, rad(44.99))
	Turn(luparm, x_axis, 0, rad(44.99))
	WaitForTurn(torso, y_axis)
	WaitForTurn(ruparm, x_axis)
	WaitForTurn(luparm, x_axis)
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	RestorePosition()
end

function script.AimWeapon(num, heading, pitch)
	if num ~= 3 and bigGunAimed then return false end
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, rad(299.93))
	if num == 3 then
		bigGunAimed = true
		Turn(ruparm, x_axis, -pitch - rad(24), rad(89.98))
		WaitForTurn(ruparm, x_axis)
	else
		Turn(luparm, x_axis, -pitch - rad(30), rad(89.98))
		WaitForTurn(luparm, x_axis)
	end
	WaitForTurn(torso, y_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0
end

function script.QueryWeapon(num)
	return (num == 3) and rbigflash or lfirept     -- COB: pieces 3 / 6
end

function script.FireWeapon(num)
end

local function BuildAim(heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, rad(299.93))
	Turn(luparm, x_axis, -pitch - rad(30), rad(89.98))
	WaitForTurn(torso, y_axis)
	WaitForTurn(luparm, x_axis)
	SetUnitValue(COB.INBUILDSTANCE, 1)
end

function script.StartBuilding(heading, pitch)
	StartThread(BuildAim, heading, pitch)
end

local function StopBuild()
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	RestorePosition()
end

function script.StopBuilding()
	SetUnitValue(COB.INBUILDSTANCE, 0)
	StartThread(StopBuild)
end

function script.QueryNanoPiece()
	return nanospray              -- COB: piece 4
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

function script.Killed(recentDamage, maxHealth)
	return 1
end
