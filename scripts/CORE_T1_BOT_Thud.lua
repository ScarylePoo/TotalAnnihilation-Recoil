-- Thud (CORE_T1_BOT_Thud): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's CORE_T1_BOT_Thud.COB: torso 90 deg/s, gun cradle pitches at 45 deg/s, restore after a fixed
-- 2750 ms, the two barrels alternate (5 elmo recoil at 150, back at 10 elmo/s; the next shot waits for the recoil
-- like the COB's wait-move), same death table and corpse types. The walk is the shared one (scripts/headers/walk.lua);
-- the 1998 muzzle-flash show/hide of the firepoints is gone.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, gun, rgun, rfirept, lgun, lfirept = piece('ground', 'torso', 'gun', 'rgun', 'rfirept', 'lgun', 'lfirept')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 4
local barrel = 0                 -- COB static 3: 0 = right barrel fires next

function script.Create()
	StartThread(SmokeUnit, {torso, pelvis})
end

local function RestoreAfterDelay()
	Sleep(2750)
	Turn(torso, y_axis, 0, rad(90))
	Turn(gun, x_axis, 0, rad(45))
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, rad(90))
	Turn(gun, x_axis, -pitch, rad(45))
	WaitForTurn(torso, y_axis)
	WaitForTurn(gun, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0
end

function script.QueryWeapon(num)
	return (barrel == 0) and rfirept or lfirept
end

function script.FireWeapon(num)
	local g = (barrel == 0) and rgun or lgun
	Move(g, z_axis, -5, 150)
	WaitForMove(g, z_axis)
	barrel = 1 - barrel
	Move(g, z_axis, 0, 10)
	WaitForMove(g, z_axis)
end

function script.SweetSpot(num)
	return torso
end

local DEATH = {ground, lfirept, lfoot, lgun, lleg, lthigh, pelvis, rfirept, rfoot, rgun, rleg, rthigh}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	Explode(torso, SFX.NONE)
	if severity <= 25 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.NONE) end
		Explode(gun, SFX.NONE)
		return 1
	elseif severity <= 50 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.FALL) end
		Explode(gun, SFX.SHATTER)
		return 2
	end
	local f = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	for _, p in ipairs(DEATH) do Explode(p, f) end
	Explode(gun, SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0))
	return 3
end
