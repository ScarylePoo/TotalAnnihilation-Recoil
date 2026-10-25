-- Crasher (CORE_T1_BOT_Crasher): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from the COB that drove the third-party model. Its only weapon is the def's weapons[3] (the COB used the
-- Tertiary call-ins): turret 225 deg/s, missile drum (gunbase) pitches at 45 deg/s, aim from the turret, restore after
-- 5x the weapon's reload time (COB SetMaxReloadTime: delay = reload ms * 5), tubes alternate gun1 / gun2 with 3.75 elmo recoil. QueryTertiary in the COB always
-- returned firept1 (both its tests check "== 0" after toggling, a TA bug): kept as-is, so missiles leave from
-- firept1 while the recoil alternates. SweetSpot = pelvis. Same death table and corpse types.
-- The walk is the shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, turret, gunbase, gun1, firept1, gun2, firept2 = piece('ground', 'turret', 'gunbase', 'gun1', 'firept1', 'gun2', 'firept2')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 4
local restoreDelay = 3000
local tube = 0                   -- COB static 0

function script.Create()
	local wd = UnitDefs[unitDefID].weapons[3] or UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 5000
	end
	StartThread(SmokeUnit, {turret, pelvis})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	SetSignalMask(0)
	Turn(turret, y_axis, 0, rad(90))
	Turn(gunbase, x_axis, 0, rad(90))
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(turret, y_axis, heading, rad(225))
	Turn(gunbase, x_axis, -pitch, rad(45))
	WaitForTurn(turret, y_axis)
	WaitForTurn(gunbase, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return turret                 -- COB: piece 2
end

function script.QueryWeapon(num)
	return firept1                -- COB: always piece 0 (see header)
end

function script.FireWeapon(num)
	local g = (tube == 0) and gun1 or gun2
	tube = 1 - tube
	Move(g, z_axis, -3.75, 62.5)
	WaitForMove(g, z_axis)
	Move(g, z_axis, 0, 7.5)
end

function script.SweetSpot(num)
	return pelvis                 -- COB: piece 4
end

local DEATH = {firept1, firept2, ground, gun1, gun2, lleg, rleg}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	Explode(pelvis, SFX.NONE); Explode(turret, SFX.NONE)
	if severity <= 25 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.NONE) end
		Explode(gunbase, SFX.NONE)
		return 1
	elseif severity <= 50 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.FALL) end
		Explode(gunbase, SFX.NONE)
		return 2
	end
	local f = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	for _, p in ipairs(DEATH) do Explode(p, f) end
	Explode(gunbase, (severity > 99) and (SFX.SHATTER + SFX.EXPLODE_ON_HIT) or SFX.NONE)
	return 3
end
