-- A.K. (CORE_T1_BOT_Ak): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from the COB that drove the third-party conscript model: torso 225 deg/s, both shoulder pods pitch at
-- 75 deg/s, restore after a fixed 2750 ms (torso 90, pods 45 deg/s), guns alternate rfire / lfire, aims from the
-- torso; same death table and corpse types (rcalf / lcalf are the standard skeleton's rleg / lleg now). The COB's
-- walk moved the pods and guns along with the step; the shared walk (scripts/headers/walk.lua) replaces all of it.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
torso, lshoulder, lgun, lfire, rshoulder, rgun, rfire = piece('torso', 'lshoulder', 'lgun', 'lfire', 'rshoulder', 'rgun', 'rfire')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 4
local gun = 0                    -- COB static 3: 0 = right gun fires next

function script.Create()
	StartThread(SmokeUnit, {torso, pelvis})
end

local function RestoreAfterDelay()
	Sleep(2750)
	Turn(torso, y_axis, 0, rad(90))
	Turn(rshoulder, x_axis, 0, rad(45))
	Turn(lshoulder, x_axis, 0, rad(45))
	WaitForTurn(torso, y_axis)
	WaitForTurn(rshoulder, x_axis)
	WaitForTurn(lshoulder, x_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(torso, y_axis, heading, rad(225))
	Turn(lshoulder, x_axis, -pitch, rad(75))
	Turn(rshoulder, x_axis, -pitch, rad(75))
	WaitForTurn(torso, y_axis)
	WaitForTurn(lshoulder, x_axis)
	WaitForTurn(rshoulder, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0
end

function script.QueryWeapon(num)
	return (gun == 0) and rfire or lfire
end

function script.FireWeapon(num)
	Sleep(100)
	gun = 1 - gun
end

function script.SweetSpot(num)
	return torso
end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		for _, p in ipairs({lleg, lgun, lthigh, lshoulder, pelvis, rleg, rgun, rthigh, rshoulder, torso}) do
			Explode(p, SFX.NONE)
		end
		return 1
	elseif severity <= 50 then
		for _, p in ipairs({lgun, lshoulder, pelvis, rgun, rshoulder}) do Explode(p, SFX.FALL) end
		Explode(torso, SFX.SHATTER)
		return 2
	end
	local burn = SFX.FALL + SFX.SMOKE + SFX.FIRE
	Explode(lgun, burn + SFX.EXPLODE_ON_HIT)
	Explode(rshoulder, burn + SFX.EXPLODE_ON_HIT)
	for _, p in ipairs({lthigh, lshoulder, pelvis, rgun, rthigh}) do Explode(p, burn) end
	Explode(torso, SFX.SHATTER)
	return 3
end
