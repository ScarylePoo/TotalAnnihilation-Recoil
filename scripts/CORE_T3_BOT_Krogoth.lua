-- Krogoth (CORE_T3_BOT_Krogoth): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's CORE_T3_BOT_Krogoth.COB: same aim/restore speeds, poses, alternating guns and silos, death table.
-- The walk is the shared one (scripts/headers/walk.lua), replacing the COB's walk/walklegs/MotionControl and with them
-- its "cannot aim until the arm swing ends" gate (the shared walk does not use the arms). The 1998 muzzle-flash
-- show/hide of the flare pieces is gone (the weapons' CEGs are the flash); the pieces stay as emit points.
-- COB z turns are negated here (engine "COBWTF"; handoff "COB -> Lua sign flips").

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
torso, head, eyegun, eyeflare, mpack = piece('torso', 'head', 'eyegun', 'eyeflare', 'mpack')
luparm, larm, lgunflare, ruparm, rarm, rgunflare = piece('luparm', 'larm', 'lgunflare', 'ruparm', 'rarm', 'rgunflare')
lmissle2, lmispoint, rmissle2, rmispoint = piece('lmissle2', 'lmispoint', 'rmissle2', 'rmispoint')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped({cadence = 1.35})   -- measured in the engine: at 1.0 planted feet only cover 72 % of the ground speed (probe)

local rad = math.rad
local SIG_AIM = {2, 4, 8}         -- COB: AimPrimary / AimSecondary / AimTertiary
local restoreDelay = 2000         -- COB: SetMaxReloadTime (longest reload)
local gun = 1                     -- cannons: 1 = right fires next, 2 = left
local silo = 1                    -- rockets: 1 = right fires next, 2 = left

function script.Create()
	local maxReload = 0
	for _, w in ipairs(UnitDefs[unitDefID].weapons) do
		local wd = WeaponDefs[w.weaponDef]
		if wd and wd.reload > maxReload then maxReload = wd.reload end
	end
	restoreDelay = math.max(1000, maxReload * 1000)
	StartThread(SmokeUnit, {torso})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(torso, y_axis, 0, rad(90))
	Turn(head, y_axis, 0, rad(50))
	Turn(head, x_axis, 0, rad(50))
	Turn(luparm, z_axis, 0, rad(50))
	Turn(ruparm, z_axis, 0, rad(50))
	Turn(larm, x_axis, 0, rad(50))
	Turn(rarm, x_axis, 0, rad(50))
	Turn(luparm, x_axis, 0, rad(120))
	Turn(ruparm, x_axis, 0, rad(120))
	Turn(rmissle2, z_axis, 0, rad(60))
	Turn(lmissle2, z_axis, 0, rad(60))
	Move(rmissle2, y_axis, 0, 25)
	Move(lmissle2, y_axis, 0, 25)
end

local function AimCannons(heading, pitch)
	-- silos rise with the cannons, as in the COB
	Move(rmissle2, y_axis, 15, 25)
	Move(lmissle2, y_axis, 15, 25)
	Turn(luparm, x_axis, 0, rad(120))
	Turn(ruparm, x_axis, 0, rad(120))
	WaitForTurn(luparm, x_axis)
	WaitForTurn(ruparm, x_axis)
	Turn(rmissle2, z_axis, rad(15), rad(60))
	Turn(lmissle2, z_axis, rad(-15), rad(60))
	Turn(torso, y_axis, heading, rad(100))
	Turn(luparm, z_axis, rad(45), rad(80))
	Turn(ruparm, z_axis, rad(-45), rad(80))
	Turn(rarm, x_axis, rad(-90) - pitch, rad(120))   -- the COB's cannons held level; these follow the target
	Turn(larm, x_axis, rad(-90) - pitch, rad(120))
	WaitForTurn(torso, y_axis)
	WaitForTurn(luparm, z_axis)
	WaitForTurn(ruparm, z_axis)
	WaitForTurn(rarm, x_axis)
	WaitForTurn(larm, x_axis)
end

function script.AimWeapon(num, heading, pitch)
	Signal(SIG_AIM[num])
	SetSignalMask(SIG_AIM[num])
	if num == 1 then
		AimCannons(heading, pitch)
	elseif num == 2 then
		Turn(head, y_axis, heading, rad(300))
		Turn(head, x_axis, -pitch, rad(150))
		WaitForTurn(head, y_axis)
		WaitForTurn(head, x_axis)
	end
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return (num == 3) and mpack or torso
end

function script.QueryWeapon(num)
	if num == 1 then
		return (gun == 1) and rgunflare or lgunflare
	elseif num == 2 then
		return eyeflare
	end
	return (silo == 1) and rmispoint or lmispoint
end

local function CannonKick(uparm, arm)
	Turn(uparm, x_axis, rad(85), rad(200))
	Turn(arm, x_axis, rad(-100), rad(200))
	Sleep(150)
	Turn(arm, x_axis, rad(-86), rad(100))
	Turn(uparm, x_axis, 0, rad(100))
end

function script.FireWeapon(num)
	if num == 1 then
		if gun == 1 then
			StartThread(CannonKick, ruparm, rarm)
			gun = 2
		else
			StartThread(CannonKick, luparm, larm)
			gun = 1
		end
	elseif num == 3 then
		silo = 3 - silo
	end
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 1
end

local DEATH = {eyeflare, eyegun, pelvis, larm, lgunflare, lfoot, lleg, lmispoint, lthigh, luparm, mpack,
	rarm, rgunflare, rfoot, rleg, rmispoint, rthigh, ruparm}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Explode(head, SFX.NONE)
		for _, p in ipairs(DEATH) do Explode(p, SFX.NONE) end
		Explode(torso, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Explode(head, SFX.SHATTER)
		for _, p in ipairs(DEATH) do Explode(p, SFX.FALL) end
		Explode(torso, SFX.NONE)
		return 2
	end
	Explode(head, SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0))
	local f = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	for _, p in ipairs(DEATH) do Explode(p, f) end
	Explode(torso, SFX.NONE)
	return 3
end
