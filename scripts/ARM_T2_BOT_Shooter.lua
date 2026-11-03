-- Shooter (ARM_T2_BOT_Shooter): Lua unit script for the remodelled sniper walker (standard biped skeleton).
-- Started from TA's ARM_T2_BOT_Shooter.COB; the first aim brings the rifle up (RequestState(0)), then the torso turns to the heading at 210 deg/s; after the
-- restore delay (reload * 3) the torso turns back at 200 deg/s and RequestState(1) puts the rifle down. The COB's shoulder keyframes are gone: written for
-- the 1998 model, they threw the kit rifle clear of the arm (12.9 elmo, piece_gaps.py). Now upper arm and forearm turn opposite, so the rifle rises level
-- and stays in the hand, and the barrel telescopes out of its housing. Aim/query pieces and the death table are the COB's; the old walk is replaced by the shared one.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
groundx2, torso, head, ruparm, rarm, gun, scope, sleave, barrel, flash =
	piece('groundx2', 'torso', 'head', 'ruparm', 'rarm', 'gun', 'scope', 'sleave', 'barrel', 'flash')
leftshoulder, luparm, larm, lhand = piece('leftshoulder', 'luparm', 'larm', 'lhand')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 2
local restoreDelay = 2000
local active = false          -- COB static 0: rifle shouldered

local BODY = rad(75)
local function activatescr()
	Turn(ruparm, x_axis, rad(-60), BODY)
	Turn(rarm, x_axis, rad(60), BODY)
	Turn(luparm, x_axis, rad(-45), BODY)
	Turn(larm, x_axis, rad(-35), BODY)
	Sleep(800)
	Move(barrel, z_axis, 9, 18)
	Sleep(800)
end

local function deactivatescr()
	Move(barrel, z_axis, 0, 18)
	Sleep(500)
	Turn(ruparm, x_axis, 0, BODY)
	Turn(rarm, x_axis, 0, BODY)
	Turn(luparm, x_axis, 0, BODY)
	Turn(larm, x_axis, 0, BODY)
	Sleep(800)
end
-- COB RequestState: one worker runs Go/Stop until the requested state stops changing (0 = shouldered, 1 = down)
local wanted, current, busy = 1, 1, false
local function RequestState(state)
	wanted = state
	if busy then return end
	busy = true
	while wanted ~= current do
		current = wanted
		if current == 0 then
			if not active then activatescr(); active = true end
		else
			if active then deactivatescr(); active = false end
		end
	end
	busy = false
end

function script.Create()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 3000
	end
	StartThread(SmokeUnit, {torso})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	StartThread(RequestState, 1)
	Turn(torso, y_axis, 0, rad(199.95))
	Turn(torso, x_axis, 0, rad(100))
end

function script.AimWeapon(num, heading, pitch)
	StartThread(RequestState, 0)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	while not active do
		Sleep(350)
	end
	Turn(torso, y_axis, heading, rad(209.95))
	Turn(torso, x_axis, -pitch, rad(150))       -- not in the COB, whose rifle ignored pitch
	WaitForTurn(torso, y_axis)
	WaitForTurn(torso, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

local function Kick()
	Turn(rarm, x_axis, rad(52), rad(200))       -- muzzle kicks up
	Sleep(150)
	Turn(rarm, x_axis, rad(60), rad(50))
end

function script.FireWeapon(num)
	StartThread(Kick)
end

function script.AimFromWeapon(num)
	return gun                    -- the engine's pitch is measured from here; the rifle is carried far below the torso (the COB's piece 1)
end

function script.QueryWeapon(num)
	return flash                  -- COB: piece 0
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 1
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({barrel, gun, head, pelvis, larm, lhand, lleg, luparm, lthigh, rarm, rleg, ruparm, rthigh, scope, sleave, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({barrel, gun, head, pelvis, larm, lhand, lleg, luparm, lthigh, rarm, rleg, ruparm, rthigh, scope, sleave}, SFX.FALL)
		Blow({torso}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({barrel, gun, head, pelvis, larm, lhand, lleg, luparm, lthigh, rarm, rleg, ruparm, rthigh, scope, sleave}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({torso}, SFX.SHATTER)
		return 2
	end
	Blow({barrel, gun, head, pelvis, larm, lhand, lleg, luparm, lthigh, rarm, rleg, ruparm, rthigh, scope, sleave}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 2
end
