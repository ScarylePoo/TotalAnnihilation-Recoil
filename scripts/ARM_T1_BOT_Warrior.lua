-- Warrior (ARM_T1_BOT_Warrior): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T1_BOT_Warrior.COB: weapon 1 (laser cannon, right arm) pitches ruparm, weapon 2 (EMG, left
-- arm) pitches luparm, both turn the torso at 150 deg/s and pitch at 200 deg/s and share one aim signal like the COB;
-- restore after the delay (torso 90, arms 45 deg/s); same death table and corpse types.
-- TA's hips / l_thigh / r_thigh walk pieces are replaced by the standard skeleton; the walk is the shared one
-- (scripts/headers/walk.lua). The 1998 muzzle-flash show/hide of gunflare is gone; emit pieces are kept.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
groundx2, torso, head, luparm, larm, lemg, emgflare, ruparm, rarm, rgun, gunflare =
	piece('groundx2', 'torso', 'head', 'luparm', 'larm', 'lemg', 'emgflare', 'ruparm', 'rarm', 'rgun', 'gunflare')

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
	Turn(ruparm, x_axis, 0, rad(45))
	Turn(rarm, y_axis, 0, rad(45))
	Turn(luparm, x_axis, 0, rad(45))
	WaitForTurn(torso, y_axis)
	WaitForTurn(ruparm, x_axis)
	WaitForTurn(rarm, y_axis)
	WaitForTurn(luparm, x_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	local arm = (num == 1) and ruparm or luparm
	Turn(torso, y_axis, heading, rad(150))
	Turn(arm, x_axis, -pitch, rad(200))
	WaitForTurn(torso, y_axis)
	WaitForTurn(arm, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0 for both weapons
end

function script.QueryWeapon(num)
	return (num == 1) and gunflare or emgflare
end

function script.FireWeapon(num)
end

function script.SweetSpot(num)
	return torso
end

local DEATH = {lemg, lfoot, lleg, larm, lthigh, luparm, rgun, rfoot, rleg, rarm, rthigh, ruparm}

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
