-- Peewee (ARM_T1_BOT_Peewee): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T1_BOT_Peewee.COB: same aim/restore speeds, idle pose, alternating guns and death table.
-- The walk is the shared one (scripts/headers/walk.lua); the 1998 muzzle-flash show/hide of rfire/lfire is gone
-- (the weapon's CEG is the flash), the pieces stay as emit points.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, luparm, lloarm, lfire, ruparm, rloarm, rfire = piece('ground', 'torso', 'luparm', 'lloarm', 'lfire', 'ruparm', 'rloarm', 'rfire')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 1
local IDLE_ARM = rad(90)          -- forearms hang down when not aiming (COB: turn ?loarm to x-axis <90>)
local restoreDelay = 3000         -- COB: SetMaxReloadTime -> reload * 2
local aiming = false
local gun = 0                     -- 0 = right gun fires next, 1 = left

function script.Create()
	Turn(rloarm, x_axis, IDLE_ARM)
	Turn(lloarm, x_axis, IDLE_ARM)
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = math.max(1000, WeaponDefs[wd.weaponDef].reload * 2000)
	end
	StartThread(SmokeUnit, {torso, pelvis})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	-- COB: torso 90 deg/s, arms 45 deg/s
	Turn(torso, y_axis, 0, rad(90))
	Turn(rloarm, x_axis, IDLE_ARM, rad(45))
	Turn(lloarm, x_axis, IDLE_ARM, rad(45))
	Turn(ruparm, x_axis, 0, rad(45))
	Turn(luparm, x_axis, 0, rad(45))
	aiming = false
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	aiming = true
	Turn(torso, y_axis, heading, rad(150))
	Turn(lloarm, x_axis, 0, rad(200))
	Turn(rloarm, x_axis, 0, rad(200))
	Turn(luparm, x_axis, -pitch, rad(200))
	Turn(ruparm, x_axis, -pitch, rad(200))
	WaitForTurn(torso, y_axis)
	WaitForTurn(lloarm, x_axis)
	WaitForTurn(rloarm, x_axis)
	WaitForTurn(luparm, x_axis)
	WaitForTurn(ruparm, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return (gun == 0) and ruparm or luparm
end

function script.QueryWeapon(num)
	return (gun == 0) and rfire or lfire
end

function script.FireWeapon(num)
	gun = 1 - gun
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local DEATH = {ground, lfire, lfoot, lleg, lloarm, lthigh, luparm, pelvis, rfire, rfoot, rleg, rloarm, rthigh, ruparm}

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
