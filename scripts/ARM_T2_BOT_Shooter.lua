-- Shooter (ARM_T2_BOT_Shooter): Lua unit script for the remodelled sniper walker (standard biped skeleton).
-- Started from TA's ARM_T2_BOT_Shooter.COB, but the rifle handling is new. Idle it carries the rifle forward at the waist; the first aim (RequestState(0)) shoulders it
-- in 0.8 s, level throughout (ruparm + rarm + gun sum to 0), the left hand comes to the receiver and the barrel telescopes out. The torso then turns to the heading and
-- pitch. After the restore delay (reload * 3) it returns. Aim/query pieces and the death table are the COB's; the old walk is replaced by the shared one.

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

-- right arm poses: {ruparm, rarm, gun} x turns in degrees. gun = -(ruparm + rarm), so the rifle stays level
local IDLE = {-15, -60, 75}
local AIM = {-22.9, -96.2, 119.1}
local UP_TIME = 0.8           -- s

local function Pose(p, time)
	Turn(ruparm, x_axis, rad(p[1]), time and math.abs(rad(AIM[1] - IDLE[1])) / time or nil)
	Turn(rarm, x_axis, rad(p[2]), time and math.abs(rad(AIM[2] - IDLE[2])) / time or nil)
	Turn(gun, x_axis, rad(p[3]), time and math.abs(rad(AIM[3] - IDLE[3])) / time or nil)
end

local function activatescr()
	Pose(AIM, UP_TIME)
	Turn(leftshoulder, y_axis, rad(-62), rad(62 / UP_TIME))
	Turn(luparm, x_axis, rad(-78), rad(78 / UP_TIME))
	Turn(larm, x_axis, rad(-14), rad(14 / UP_TIME))
	Sleep(800)
	Move(barrel, z_axis, 9, 18)
	Sleep(500)
end

local function deactivatescr()
	Move(barrel, z_axis, 0, 18)
	Sleep(500)
	Pose(IDLE, UP_TIME)
	Turn(leftshoulder, y_axis, 0, rad(62 / UP_TIME))
	Turn(luparm, x_axis, 0, rad(78 / UP_TIME))
	Turn(larm, x_axis, 0, rad(14 / UP_TIME))
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
	Pose(IDLE)
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
	Move(gun, z_axis, -1.6)                     -- recoil into the shoulder
	Sleep(120)
	Move(gun, z_axis, 0, 6)
end

function script.FireWeapon(num)
	StartThread(Kick)
end

function script.AimFromWeapon(num)
	return gun                    -- the engine's pitch is measured from here; the rifle sits off to the side of the torso (the COB's piece 1)
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
