-- Flea (ARM_T1_BOT_Flea): Lua unit script for the remodelled walker (standard QUAD skeleton).
-- Ported from TA's ARM_T1_BOT_Flea.COB: turret 250 deg/s to aim, back at 150 deg/s after the restore delay, fires
-- from barrel's `flare`, aims from the turret; same death table and corpse types (the old leg pieces rrleg/lrleg map
-- to the new back legs rbleg/lbleg). The COB's walk also nodded the head; the shared quad walk
-- (scripts/headers/walk.lua) replaces the whole old walk, so the head now stays still.

pelvis, legs = piece('pelvis', 'legs')
rfthigh, rfleg, rffoot, lfthigh, lfleg, lffoot = piece('rfthigh', 'rfleg', 'rffoot', 'lfthigh', 'lfleg', 'lffoot')
rbthigh, rbleg, rbfoot, lbthigh, lbleg, lbfoot = piece('rbthigh', 'rbleg', 'rbfoot', 'lbthigh', 'lbleg', 'lbfoot')
groundx1, body, head, turret, barrel, flare = piece('groundx1', 'body', 'head', 'turret', 'barrel', 'flare')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Quad()

local rad = math.rad
local SIG_AIM = 2
local restoreDelay = 3000

function script.Create()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {body, turret})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(turret, y_axis, 0, rad(150))
	WaitForTurn(turret, y_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	Turn(turret, y_axis, heading, rad(250))
	WaitForTurn(turret, y_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return turret                 -- COB: piece 1
end

function script.QueryWeapon(num)
	return flare                  -- COB: piece 2
end

function script.FireWeapon(num)
end

function script.SweetSpot(num)
	return body                   -- COB: piece 0
end

local LEGS = {rbleg, rfleg, lbleg, lfleg}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	local burn = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	Explode(turret, burn)
	if severity <= 25 then
		Explode(barrel, SFX.NONE)
		for _, p in ipairs(LEGS) do Explode(p, SFX.NONE) end
		Explode(body, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Explode(barrel, SFX.FALL)
		for _, p in ipairs(LEGS) do Explode(p, SFX.FALL) end
		Explode(body, SFX.FALL)
		return 2
	end
	Explode(barrel, burn)
	for _, p in ipairs(LEGS) do Explode(p, burn) end
	Explode(body, (severity > 99) and (SFX.SHATTER + SFX.EXPLODE_ON_HIT) or burn)
	return 3
end
