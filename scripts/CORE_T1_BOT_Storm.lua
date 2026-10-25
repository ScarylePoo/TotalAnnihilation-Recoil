-- Storm (CORE_T1_BOT_Storm): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from the COB that drove the third-party model: the whole torso turns (90 deg/s) and pitches (45 deg/s) to
-- aim, restores after a fixed 5000 ms, rockets alternate rbarrel2 / lbarrel2, aim from the torso; same death table
-- and corpse types (lcalf / rcalf are the standard skeleton's lleg / rleg now). The walk is the shared one.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
torso, lgun, lbarrel1, lbarrel2, rexhaust, rgun, rbarrel1, rbarrel2, lexhaust =
	piece('torso', 'lgun', 'lbarrel1', 'lbarrel2', 'rexhaust', 'rgun', 'rbarrel1', 'rbarrel2', 'lexhaust')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 4
local tube = 0                   -- COB static 0: 0 = rbarrel2 fires next

function script.Create()
	StartThread(SmokeUnit, {torso, pelvis})
end

local function RestoreAfterDelay()
	Sleep(5000)
	Turn(torso, y_axis, 0, rad(90))
	Turn(torso, x_axis, 0, rad(45))
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, rad(90))
	Turn(torso, x_axis, -pitch, rad(45))
	WaitForTurn(torso, y_axis)
	WaitForTurn(torso, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0
end

function script.QueryWeapon(num)
	return (tube == 0) and rbarrel2 or lbarrel2
end

function script.FireWeapon(num)
	tube = 1 - tube
end

function script.SweetSpot(num)
	return torso
end

local DEATH = {lfoot, lleg, lthigh, pelvis, rfoot, rleg, rthigh, torso}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.NONE) end
		return 1
	elseif severity <= 50 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.FALL) end
		return 2
	end
	for _, p in ipairs(DEATH) do Explode(p, SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT) end
	return 3
end
