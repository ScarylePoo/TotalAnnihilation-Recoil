-- Morty (CORE_T2_BOT_Morty): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's CORE_T2_BOT_Morty.COB: the torso turns at 190 deg/s and the mortar cradle (support) pitches at
-- 150 deg/s to aim; after the restore delay (reload * 2) they return at 90 / 45 deg/s. Each shot slams the tube back
-- 12.5 elmo, rocks the torso back 10 deg after 150 ms, then recovers (torso 20 deg/s, tube 7.5 elmo/s). Fires from
-- flare, aims from the support, SweetSpot = torso, same death table and corpse types (old thigh1/leg1/foot1 = the
-- left leg, thigh2.. = the right). The old walk is replaced by the shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, cod, torso, head, eye, shoulder, support, barrel, flare =
	piece('ground', 'cod', 'torso', 'head', 'eye', 'shoulder', 'support', 'barrel', 'flare')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 2
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
	Turn(support, x_axis, 0, rad(44.99))
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, rad(189.99))
	Turn(support, x_axis, -pitch, rad(149.99))
	WaitForTurn(torso, y_axis)
	WaitForTurn(support, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

local function Recoil()
	Move(barrel, z_axis, -12.5, 1250)
	Sleep(150)
	Turn(torso, x_axis, rad(-10), rad(499.99))
	Sleep(150)
	Turn(torso, x_axis, 0, rad(20))
	Move(barrel, z_axis, 0, 7.5)
end

function script.FireWeapon(num)
	StartThread(Recoil)
end

function script.AimFromWeapon(num)
	return support                -- COB: piece 0
end

function script.QueryWeapon(num)
	return flare                  -- COB: piece 1
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 4
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({barrel, lfoot, rfoot, lleg, rleg, support, lthigh, rthigh, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({barrel}, SFX.NONE)
		Blow({lfoot, rfoot, lleg, rleg, support, lthigh, rthigh}, SFX.FALL)
		Blow({torso}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({barrel}, SFX.NONE)
		Blow({lfoot, rfoot, lleg, rleg, support, lthigh, rthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({torso}, SFX.SHATTER)
		return 3
	end
	Blow({barrel}, SFX.NONE)
	Blow({lfoot, rfoot, lleg, rleg, support, lthigh, rthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({torso}, SFX.SHATTER)
	return 3
end
