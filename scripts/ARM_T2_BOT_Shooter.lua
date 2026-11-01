-- Shooter (ARM_T2_BOT_Shooter): Lua unit script for the remodelled sniper walker (standard biped skeleton).
-- Ported from TA's ARM_T2_BOT_Shooter.COB: the first aim runs RequestState(0) -> activatescr (the rifle is shouldered:
-- arms up, rifle level, the barrel housing flips round, the barrel telescopes 9 elmo, the scope drops in), then the
-- torso turns to the heading at 210 deg/s; after the restore delay (reload * 3) the torso turns back at 200 deg/s and
-- RequestState(1) -> deactivatescr puts the rifle down. Each shot kicks the gun arm (rarm x -40 at 200 deg/s, back to
-- -23 at 50 deg/s). Keyframes/speeds/sleeps, aim/query pieces and the death table are the COB's; turn-z values are
-- sign-flipped (Recoil CobInstance.h "COBWTF") and zero-speed COB moves/turns (no-ops) are left out. The old walk
-- (which also bobbed the head and arms) is replaced by the shared one.

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

local function activatescr()
	Move(head, y_axis, 0)
	Move(larm, y_axis, 0)
	Move(flash, z_axis, -0.25)
	Turn(torso, x_axis, rad(0))
	Turn(torso, x_axis, rad(-3.5), rad(13.5))
	Turn(ruparm, x_axis, rad(0))
	Turn(ruparm, x_axis, rad(17.59), rad(67.58))
	Turn(rarm, x_axis, rad(0))
	Turn(rarm, x_axis, rad(-65.78), rad(252.83))
	Sleep(260)
	Turn(torso, x_axis, rad(-8.79), rad(18.79))
	Turn(ruparm, x_axis, rad(-11.59), rad(104.17))
	Turn(head, x_axis, rad(-8.39), rad(30.09))
	Turn(rarm, x_axis, rad(-97.37), rad(112.97))
	Sleep(280)
	Move(gun, y_axis, -2.75, 11)
	Turn(torso, x_axis, rad(-2.5), rad(24.29))
	Turn(ruparm, x_axis, rad(-46.08), rad(132.47))
	Turn(head, x_axis, rad(-4.89), rad(13.5))
	Turn(leftshoulder, y_axis, rad(-10.5), rad(40.58))
	Turn(luparm, x_axis, rad(-60.78), rad(233.94))
	Turn(larm, z_axis, rad(-24.99), rad(95.98))
	Turn(lhand, z_axis, rad(-24.29), rad(93.27))
	Turn(rarm, x_axis, rad(-59.08), rad(147.35))
	Turn(gun, x_axis, rad(-44.99), rad(173.05))
	Sleep(260)
	Move(leftshoulder, z_axis, 4.5, 18.75)
	Move(luparm, y_axis, -1, 4.25)
	Move(larm, y_axis, -1.25, 4.75)
	Move(gun, z_axis, 2, 7.75)
	Turn(torso, x_axis, rad(-1.09), rad(5.89))
	Turn(ruparm, x_axis, rad(-66.77), rad(86.37))
	Turn(head, x_axis, rad(-1.79), rad(13.19))
	Turn(leftshoulder, y_axis, rad(-27.09), rad(68.87))
	Turn(luparm, x_axis, rad(-89.67), rad(120.06))
	Turn(larm, z_axis, rad(-34.49), rad(39.58))
	Turn(lhand, z_axis, rad(-27.38), rad(13.19))
	Turn(rarm, x_axis, rad(-23.19), rad(149.46))
	Turn(gun, x_axis, rad(-89.98), rad(187.45))
	Sleep(240)
	Move(leftshoulder, z_axis, 4.75, 1.25)
	Move(luparm, y_axis, -1.25, 1.25)
	Turn(leftshoulder, y_axis, rad(-27.38), rad(3.59))
	Turn(luparm, x_axis, rad(-89.98), rad(3.59))
	Turn(larm, z_axis, rad(-35.18), rad(7.19))
	Turn(lhand, z_axis, rad(-43.18), rad(161.46))
	Sleep(98)
	Turn(sleave, x_axis, rad(44.99), rad(416.69))
	Sleep(108)
	Turn(sleave, x_axis, rad(179.96), rad(2812.51))
	Sleep(48)
	Move(barrel, z_axis, 9, 117)
	Sleep(78)
	Move(scope, y_axis, -1.75, 11.75)
	Turn(scope, x_axis, rad(-19.29), rad(140.06))
	Sleep(138)
	Move(scope, y_axis, -2.75, 8.5)
	Turn(scope, x_axis, rad(0), rad(130.66))
	Sleep(148)
	Sleep(18)
end

local function deactivatescr()
	Move(head, y_axis, 0)
	Move(leftshoulder, z_axis, 4.75)
	Move(leftshoulder, z_axis, 2.75, 10)
	Move(luparm, y_axis, -1.25)
	Move(larm, y_axis, -1.25)
	Move(gun, y_axis, -2.75)
	Move(gun, z_axis, 2)
	Move(scope, y_axis, -2.75)
	Move(scope, y_axis, -1.75, 6.25)
	Move(barrel, z_axis, 9)
	Move(barrel, z_axis, 0, 45.5)
	Turn(torso, x_axis, rad(-1.09))
	Turn(ruparm, x_axis, rad(-66.77))
	Turn(ruparm, x_axis, rad(-40.78), rad(130.06))
	Turn(head, x_axis, rad(-1.79))
	Turn(leftshoulder, y_axis, rad(-27.38))
	Turn(leftshoulder, y_axis, rad(-6.29), rad(105.47))
	Turn(luparm, x_axis, rad(-89.98))
	Turn(luparm, x_axis, rad(-59.38), rad(152.96))
	Turn(larm, z_axis, rad(-35.18))
	Turn(larm, z_axis, rad(-19.29), rad(79.07))
	Turn(lhand, z_axis, rad(-43.18))
	Turn(lhand, z_axis, rad(-26.38), rad(84.37))
	Turn(rarm, x_axis, rad(-23.19))
	Turn(gun, x_axis, rad(-89.98))
	Turn(scope, x_axis, rad(0))
	Turn(scope, x_axis, rad(-18.29), rad(91.37))
	Turn(sleave, x_axis, rad(179.96))
	Sleep(200)
	Move(leftshoulder, z_axis, 0, 13.25)
	Move(larm, y_axis, 0, 5.5)
	Move(scope, y_axis, 0, 8.25)
	Turn(ruparm, x_axis, rad(-29.88), rad(54.49))
	Turn(leftshoulder, y_axis, rad(0), rad(31.59))
	Turn(luparm, x_axis, rad(-40.78), rad(93.17))
	Turn(larm, z_axis, rad(-10.19), rad(45.68))
	Turn(lhand, z_axis, rad(-13), rad(66.77))
	Turn(scope, x_axis, rad(0), rad(91.37))
	Sleep(200)
	Move(luparm, y_axis, 0, 5.5)
	Turn(ruparm, x_axis, rad(-48.88), rad(94.87))
	Turn(luparm, x_axis, rad(-25.69), rad(75.57))
	Turn(larm, z_axis, rad(0), rad(50.99))
	Turn(lhand, z_axis, rad(0), rad(64.98))
	Turn(sleave, x_axis, rad(89.98), rad(449.98))
	Sleep(200)
	Turn(ruparm, x_axis, rad(-13.69), rad(175.75))
	Turn(luparm, x_axis, rad(-1.09), rad(123.06))
	Turn(larm, x_axis, rad(-24.29), rad(121.26))
	Turn(sleave, x_axis, rad(0), rad(449.98))
	Sleep(200)
	Move(gun, y_axis, 0, 14.25)
	Turn(ruparm, x_axis, rad(0), rad(68.58))
	Turn(larm, x_axis, rad(-11.59), rad(63.28))
	Turn(rarm, x_axis, rad(-26.38), rad(15.79))
	Turn(gun, x_axis, rad(-20.39), rad(348.01))
	Sleep(200)
	Move(gun, z_axis, 0, 9.5)
	Turn(luparm, x_axis, rad(0), rad(5.29))
	Turn(larm, x_axis, rad(0), rad(57.99))
	Turn(rarm, x_axis, rad(-4.89), rad(107.27))
	Turn(gun, x_axis, rad(20.39), rad(203.95))
	Sleep(200)
	Turn(rarm, x_axis, rad(0), rad(24.59))
	Turn(gun, x_axis, rad(0), rad(101.98))
	Sleep(200)
	Sleep(200)
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
end

function script.AimWeapon(num, heading, pitch)
	StartThread(RequestState, 0)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	while not active do
		Sleep(350)
	end
	Turn(torso, y_axis, heading, rad(209.95))
	WaitForTurn(torso, y_axis)
	StartThread(RestoreAfterDelay)
	return true
end

local function Kick()
	Turn(rarm, x_axis, rad(-39.99), rad(199.95))
	Sleep(150)
	Turn(rarm, x_axis, rad(-22.99), rad(49.99))
end

function script.FireWeapon(num)
	StartThread(Kick)
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 1
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
		return 3
	end
	Blow({barrel, gun, head, pelvis, larm, lhand, lleg, luparm, lthigh, rarm, rleg, ruparm, rthigh, scope, sleave}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({torso}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
