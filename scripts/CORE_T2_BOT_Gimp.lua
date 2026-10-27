-- Gimp (CORE_T2_BOT_Gimp): Lua unit script for the remodelled amphibious walker (standard biped skeleton).
-- Ported from TA's CORE_T2_BOT_Gimp.COB: both weapons only turn the gun bar (head) to the heading at 100 deg/s and
-- return it at 90 deg/s after the restore delay (reload * 2); the cannon fires from gunflare, the laser from
-- laserflare, both aim from the head, SweetSpot = body. While moving it emits bubbles (sfx 259) under water and wakes
-- (sfx 3) at the surface/shore every 250 ms by setSFXoccupy, from the feet, legs and body as the COB did (the feet and
-- legs are the skeleton's now). Death table and corpse types are the COB's. The old walk is replaced by the shared one.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
groundx2, body, head, laser, laserflare, gun, gunflare = piece('groundx2', 'body', 'head', 'laser', 'laserflare', 'gun', 'gunflare')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()
local WalkStart, WalkStop = script.StartMoving, script.StopMoving

local rad = math.rad
local SIG_SFX, SIG_AIM = 2, 4
local restoreDelay = 3000
local terrain = 4             -- COB static 5 (setSFXoccupy)

function script.setSFXoccupy(t)
	terrain = t
end

local function MoveSfx()
	Signal(SIG_SFX)
	SetSignalMask(SIG_SFX)
	while true do
		if terrain == 3 then
			EmitSfx(lfoot, 259); EmitSfx(rfoot, 259); EmitSfx(body, 259)
		end
		if terrain == 2 then
			EmitSfx(lfoot, 259); EmitSfx(rfoot, 259)
			EmitSfx(lleg, 3); EmitSfx(rleg, 3); EmitSfx(body, 3)
		end
		if terrain == 1 then
			EmitSfx(lfoot, 3); EmitSfx(rfoot, 3)
		end
		Sleep(250)
	end
end

function script.StartMoving()
	WalkStart()
	StartThread(MoveSfx)
end

function script.StopMoving()
	WalkStop()
	Signal(SIG_SFX)
end

function script.Create()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {body})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(head, y_axis, 0, rad(90))
	WaitForTurn(head, y_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(head, y_axis, heading, rad(100))
	WaitForTurn(head, y_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return head                   -- COB: piece 3
end

function script.QueryWeapon(num)
	return (num == 1) and gunflare or laserflare   -- COB: pieces 1 / 2
end

function script.FireWeapon(num)
end

function script.SweetSpot(num)
	return body                   -- COB: piece 0
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({body, gun, head, pelvis, lfoot, lleg, rfoot, rleg}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({body}, SFX.NONE)
		Blow({gun, pelvis, lfoot, lleg, rfoot, rleg}, SFX.FALL)
		Blow({head}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({body}, SFX.NONE)
		Blow({gun, pelvis, lfoot, lleg, rfoot, rleg}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({head}, SFX.SHATTER)
		return 3
	end
	Blow({body}, SFX.NONE)
	Blow({gun, pelvis, lfoot, lleg, rfoot, rleg}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({head}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
