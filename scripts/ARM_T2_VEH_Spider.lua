-- Spider (ARM_T2_VEH_Spider): Lua unit script for the remodelled hexapod (shared six-leg skeleton).
-- Ported from TA's ARM_T2_VEH_Spider.COB: same aim/restore speeds, alternating emitters with the same recoil, same
-- death table (the six old leg pieces' entries go to the eighteen new leg pieces). The walk is the shared hexapod
-- tripod gait (scripts/headers/walk.lua, walk.Hexa); the 1998 muzzle-flash show/hide of flare1/flare2 is gone (the
-- weapon's CEG is the flash), the pieces stay as emit points.

pelvis, legs, base, turret, barrel1, flare1, barrel2, flare2 =
	piece('pelvis', 'legs', 'base', 'turret', 'barrel1', 'flare1', 'barrel2', 'flare2')
rfthigh, rfleg, rffoot, lfthigh, lfleg, lffoot = piece('rfthigh', 'rfleg', 'rffoot', 'lfthigh', 'lfleg', 'lffoot')
rmthigh, rmleg, rmfoot, lmthigh, lmleg, lmfoot = piece('rmthigh', 'rmleg', 'rmfoot', 'lmthigh', 'lmleg', 'lmfoot')
rbthigh, rbleg, rbfoot, lbthigh, lbleg, lbfoot = piece('rbthigh', 'rbleg', 'rbfoot', 'lbthigh', 'lbleg', 'lbfoot')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
local hexaReady = walk.Hexa()

local rad = math.rad
local SIG_AIM = 2
local restoreDelay = 3000         -- COB: 3000, then SetMaxReloadTime -> reload * 2
local gun = 0                     -- 0 = barrel1/flare1 fires next, 1 = barrel2/flare2

function script.Create()
	hexaReady()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = math.max(1000, WeaponDefs[wd.weaponDef].reload * 2000)
	end
	StartThread(SmokeUnit, {base})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(turret, y_axis, 0, rad(90))
	Turn(turret, x_axis, 0, rad(90))
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(turret, y_axis, heading, rad(90))
	Turn(turret, x_axis, -pitch, rad(90))
	WaitForTurn(turret, y_axis)
	WaitForTurn(turret, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return turret
end

function script.QueryWeapon(num)
	return (gun == 0) and flare1 or flare2
end

function script.FireWeapon(num)
	local b = (gun == 0) and barrel1 or barrel2
	gun = 1 - gun
	Move(b, z_axis, -3.125, 1250)  -- COB: snap back 3.125, recover at 7.5/s
	WaitForMove(b, z_axis)
	Move(b, z_axis, 0, 7.5)
end

function script.SweetSpot(num)
	return base
end

local LEGS = {rfthigh, rfleg, rffoot, lfthigh, lfleg, lffoot, rmthigh, rmleg, rmfoot,
	lmthigh, lmleg, lmfoot, rbthigh, rbleg, rbfoot, lbthigh, lbleg, lbfoot}
local PARTS = {barrel1, barrel2, flare1, flare2}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	Explode(base, SFX.NONE)
	if severity <= 25 then
		for _, p in ipairs(PARTS) do Explode(p, SFX.NONE) end
		for _, p in ipairs(LEGS) do Explode(p, SFX.NONE) end
		Explode(turret, SFX.NONE)
		return 1
	elseif severity <= 50 then
		for _, p in ipairs(PARTS) do Explode(p, SFX.FALL) end
		for _, p in ipairs(LEGS) do Explode(p, SFX.FALL) end
		Explode(turret, SFX.SHATTER)
		return 2
	end
	local f = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	for _, p in ipairs(PARTS) do Explode(p, f) end
	for _, p in ipairs(LEGS) do Explode(p, f) end
	Explode(turret, SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0))
	return 2
end
