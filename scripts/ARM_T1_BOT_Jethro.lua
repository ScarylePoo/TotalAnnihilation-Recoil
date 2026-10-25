-- Jethro (ARM_T1_BOT_Jethro): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T1_BOT_Jethro.COB: the missile pods split open (open/close keyframes and speeds as the COB)
-- the first time it aims and close after the restore delay; open/close cannot be interrupted by a new aim (the COB
-- drops its signal mask around them), torso 275 deg/s, alternating launchers with 3.75 elmo recoil, same death
-- table and corpse types. COB negates turn-z destinations ("COBWTF" in Recoil's CobInstance.h), so the pod angles
-- below are the COB's with the sign flipped. The walk is the shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, luparm, lloarm, lgun, lfirept, ruparm, rloarm, rgun, rfirept =
	piece('ground', 'torso', 'luparm', 'lloarm', 'lgun', 'lfirept', 'ruparm', 'rloarm', 'rgun', 'rfirept')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 4
local restoreDelay = 3000
local closed = true              -- COB static 3
local busy = false               -- COB static 4: pods moving
local gun = 0                    -- COB static 5: 0 = right launcher fires next

local function Open()
	Turn(luparm, z_axis, 0); Turn(luparm, z_axis, rad(73.48), rad(212.35))
	Turn(lloarm, z_axis, 0); Turn(lloarm, z_axis, rad(-90), rad(260.11))
	Turn(rloarm, z_axis, 0); Turn(rloarm, z_axis, rad(90), rad(260.11))
	Turn(ruparm, z_axis, 0); Turn(ruparm, z_axis, rad(-75.59), rad(218.45))
	Sleep(700)
end

local function Close()
	Turn(luparm, z_axis, rad(73.48)); Turn(luparm, z_axis, 0, rad(66.98))
	Turn(lloarm, z_axis, rad(-90)); Turn(lloarm, z_axis, 0, rad(82.04))
	Turn(rloarm, z_axis, rad(90)); Turn(rloarm, z_axis, 0, rad(82.04))
	Turn(ruparm, z_axis, rad(-75.59)); Turn(ruparm, z_axis, 0, rad(68.9))
	Sleep(2206)
end

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
	SetSignalMask(0)
	busy = true
	Close()
	Sleep(1000)
	closed = true
	busy = false
	WaitForTurn(torso, y_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	local waited = false
	while busy do
		waited = true
		Sleep(100)
	end
	if waited then                -- a restore that closed the pods meanwhile is done; drop stale aims
		SetSignalMask(0)
		Signal(SIG_AIM)
		SetSignalMask(SIG_AIM)
	end
	Turn(torso, y_axis, heading, rad(275))
	if closed then
		SetSignalMask(0)
		busy = true
		Open()
		closed = false
		busy = false
		SetSignalMask(SIG_AIM)
	end
	WaitForTurn(torso, y_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return torso                  -- COB: piece 0
end

function script.QueryWeapon(num)
	return (gun == 0) and rfirept or lfirept
end

function script.FireWeapon(num)
	if gun == 0 then
		gun = 1
		Move(rgun, z_axis, -3.75, 62.5)
		WaitForMove(rgun, z_axis)
		Move(rgun, z_axis, 0, 1.875)
	else
		gun = 0
		Move(lgun, z_axis, -3.75, 62.5)
		WaitForMove(lgun, z_axis)
		Move(lgun, z_axis, 0, 1.875)
	end
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local DEATH = {ground, lfirept, lgun, lleg, lloarm, lthigh, luparm, pelvis, rfirept, rgun, rleg, rloarm, rthigh, ruparm}

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
