-- Fido (ARM_T2_BOT_Fido): Lua unit script for the remodelled walker (standard QUAD skeleton).
-- Ported from TA's ARM_T2_BOT_Fido.COB: the turret turns at 90 deg/s and the gauss cannon pitches at 50 deg/s, both
-- return to rest after the restore delay (reload * 2); fires from `flash`, SweetSpot = gauss, same death table and
-- corpse types. The 3DO walked on its arms as front legs: the old ruparm/rloarm/rhand map to rfthigh/rfleg/rffoot,
-- the old rthigh/rleg/rfoot to rbthigh/rbleg/rbfoot (same for the left side). The COB's walk (which also swayed the
-- torso) is replaced by the shared quad walk (scripts/headers/walk.lua).

pelvis, legs = piece('pelvis', 'legs')
rfthigh, rfleg, rffoot, lfthigh, lfleg, lffoot = piece('rfthigh', 'rfleg', 'rffoot', 'lfthigh', 'lfleg', 'lffoot')
rbthigh, rbleg, rbfoot, lbthigh, lbleg, lbfoot = piece('rbthigh', 'rbleg', 'rbfoot', 'lbthigh', 'lbleg', 'lbfoot')
ground, torso, turret, gauss, flash = piece('ground', 'torso', 'turret', 'gauss', 'flash')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Quad()

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
	Turn(turret, y_axis, 0, rad(90))
	Turn(gauss, x_axis, 0, rad(50))
	WaitForTurn(turret, y_axis)
	WaitForTurn(gauss, x_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(turret, y_axis, heading, rad(90))
	Turn(gauss, x_axis, -pitch, rad(50))
	WaitForTurn(turret, y_axis)
	WaitForTurn(gauss, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return turret
end

function script.QueryWeapon(num)
	return flash                  -- COB: piece 2
end

function script.FireWeapon(num)
end

function script.SweetSpot(num)
	return gauss                  -- COB: piece 0
end

-- old arm/leg names -> the quad skeleton's front/back legs
local LIMBS = {lfthigh, lffoot, lfleg, lbthigh, lbfoot, rfthigh, rffoot, rfleg, rbthigh, rbfoot}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	for _, p in ipairs({pelvis, torso, turret}) do Explode(p, SFX.NONE) end
	if severity <= 25 then
		for _, p in ipairs(LIMBS) do Explode(p, SFX.NONE) end
		Explode(flash, SFX.NONE); Explode(gauss, SFX.NONE); Explode(ground, SFX.NONE)
		Explode(lbleg, SFX.NONE); Explode(rbleg, SFX.NONE)
		return 1
	end
	local burn = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	if severity <= 50 then
		for _, p in ipairs(LIMBS) do Explode(p, SFX.FALL) end
		Explode(flash, SFX.FALL); Explode(gauss, SFX.SHATTER); Explode(ground, SFX.FALL)
		Explode(lbleg, burn); Explode(rbleg, burn)
		return 2
	end
	for _, p in ipairs(LIMBS) do Explode(p, burn) end
	Explode(flash, burn); Explode(ground, burn); Explode(lbleg, burn); Explode(rbleg, burn)
	Explode(gauss, SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0))
	return 3
end
