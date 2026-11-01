-- Pelican (ARM_T2_BOT_Pelican): Lua unit script for the remodelled amphibious walker (standard biped skeleton).
-- Ported from TA's ARM_T2_BOT_Pelican.COB: laser turret (lasturret/lasbarrel, fires from flare) and missile pod
-- (misturret, alternating lmispoint/rmispoint) both aim at 100 deg/s and return at 90 deg/s after the restore delay
-- (reload * 2); wakes are emitted from wake1..4 every 250 ms while moving on water (setSFXoccupy 1/2); the death table
-- and corpse types are the COB's (old legs -> skeleton legs; the hip pivots are gone).
-- Water: the COB's transform/reform animated the old hip pivots, which the standard skeleton replaces. Same states
-- and triggers here (transform on setSFXoccupy 2, reform on 1 or 4), with an equivalent pose for the new legs: the legs
-- swing out sideways like outriggers (thighs z, knees straightened) and the pelvis drops 7.25 elmo (the COB's hip
-- drop), over ~1.8 s like the COB; on land the shared walk (scripts/headers/walk.lua) takes over again.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
groundx2, body, lasturret, lasbarrel, flare, misturret, rmispoint, lmispoint, pontoons =
	piece('groundx2', 'body', 'lasturret', 'lasbarrel', 'flare', 'misturret', 'rmispoint', 'lmispoint', 'pontoons')
wake1, wake2, wake3, wake4 = piece('wake1', 'wake2', 'wake3', 'wake4')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()
local WalkStart, WalkStop = script.StartMoving, script.StopMoving

local rad = math.rad
local SIG_WAKE, SIG_AIM1, SIG_AIM2, SIG_WATER = 2, 4, 8, 16
local SFX_WAKE = 2            -- COB emit-sfx 2
local restoreDelay = 3000
local moving = false
local terrain = 4             -- COB static 6 (setSFXoccupy)
local swimming = false        -- COB static 3
local missile = 0             -- COB static 4: 0 = lmispoint next

local function Transform()
	Turn(rthigh, z_axis, rad(-72), rad(170))
	Turn(lthigh, z_axis, rad(72), rad(170))
	Turn(rthigh, x_axis, 0, rad(120)); Turn(lthigh, x_axis, 0, rad(120))
	Turn(rleg, x_axis, rad(80), rad(160)); Turn(lleg, x_axis, rad(80), rad(160))
	Turn(rfoot, x_axis, rad(-35), rad(120)); Turn(lfoot, x_axis, rad(-35), rad(120))
	Move(pelvis, y_axis, -7.25, 16.744)
	Sleep(433)
	Turn(body, x_axis, rad(-8.77), rad(50.7))
	Sleep(1000)
	Turn(body, x_axis, 0, rad(120.15))
	Sleep(146)
end

local function Reform()
	Turn(rthigh, z_axis, 0, rad(400)); Turn(lthigh, z_axis, 0, rad(400))
	Turn(rleg, x_axis, 0, rad(367)); Turn(lleg, x_axis, 0, rad(371))
	Turn(rfoot, x_axis, 0, rad(306)); Turn(lfoot, x_axis, 0, rad(318))
	Move(pelvis, y_axis, 0, 24.444)
	Turn(body, x_axis, rad(-5.27), rad(23.43))
	Sleep(482)
	Turn(body, x_axis, 0, rad(15.13))
	Sleep(400)
end

local function UpdateWater()
	Signal(SIG_WATER)
	SetSignalMask(SIG_WATER)
	if terrain == 2 and not swimming then
		swimming = true
		WalkStop()
		Transform()
	elseif swimming and (terrain == 1 or terrain == 4) then
		swimming = false
		Reform()
		if moving then WalkStart() end
	end
end

function script.setSFXoccupy(t)
	terrain = t
	StartThread(UpdateWater)
end

local function Wakes()
	Signal(SIG_WAKE)
	SetSignalMask(SIG_WAKE)
	while true do
		if terrain == 2 or terrain == 1 then
			EmitSfx(wake1, SFX_WAKE); EmitSfx(wake2, SFX_WAKE); EmitSfx(wake3, SFX_WAKE); EmitSfx(wake4, SFX_WAKE)
		end
		Sleep(250)
	end
end

function script.StartMoving()
	moving = true
	if not swimming then WalkStart() end
	StartThread(Wakes)
end

function script.StopMoving()
	moving = false
	Signal(SIG_WAKE)
	if not swimming then WalkStop() end
end

function script.Create()
	Hide(pontoons)
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {body})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	Turn(lasturret, y_axis, 0, rad(90)); Turn(lasturret, x_axis, 0, rad(90))
	Turn(misturret, y_axis, 0, rad(90)); Turn(misturret, x_axis, 0, rad(90))
end

function script.AimWeapon(num, heading, pitch)
	local turret = (num == 1) and lasturret or misturret
	local sig = (num == 1) and SIG_AIM1 or SIG_AIM2
	Signal(sig)
	SetSignalMask(sig)
	Turn(turret, y_axis, heading, rad(100))
	Turn(turret, x_axis, -pitch, rad(100))
	WaitForTurn(turret, y_axis)
	WaitForTurn(turret, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return (num == 1) and lasturret or misturret      -- COB: pieces 12 / 13
end

function script.QueryWeapon(num)
	if num == 1 then return flare end                -- COB: piece 1
	return (missile == 0) and lmispoint or rmispoint  -- COB: pieces 3 / 2
end

function script.FireWeapon(num)
	if num == 2 then missile = 1 - missile end
end

function script.SweetSpot(num)
	return body                   -- COB: piece 0
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({body, lasbarrel, lasturret, lfoot, lleg, lmispoint, lthigh, misturret, pontoons, rfoot, rleg, rmispoint, rthigh, wake1, wake2, wake3, wake4}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({body, pontoons}, SFX.NONE)
		Blow({lasbarrel, lasturret, lfoot, lleg, lmispoint, lthigh, rfoot, rleg, rmispoint, rthigh, wake1, wake2, wake3, wake4}, SFX.FALL)
		Blow({misturret}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({body, pontoons}, SFX.NONE)
		Blow({lasbarrel, lasturret, lfoot, lleg, lmispoint, lthigh, rfoot, rleg, rmispoint, rthigh, wake1, wake2, wake3, wake4}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({misturret}, SFX.SHATTER)
		return 3
	end
	Blow({body, pontoons}, SFX.NONE)
	Blow({lasbarrel, lasturret, lfoot, lleg, lmispoint, lthigh, rfoot, rleg, rmispoint, rthigh, wake1, wake2, wake3, wake4}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({misturret}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
