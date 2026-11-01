-- Scarab (ARM_T2_VEH_Scarab): Lua unit script for the remodelled hexapod anti-nuke (shared six-leg skeleton).
-- Ported from TA's ARM_T2_VEH_Scarab.COB: the same open/close state machine (RequestState), the same shell and launcher
-- keyframes, aiming waits until the shell is open, the shell closes 10 s after the last aim, the hull rocks when hit,
-- same death table (the old leg and side-plate pieces' entries go to the eighteen new leg pieces). The walk is the
-- shared hexapod tripod gait (scripts/headers/walk.lua, walk.Hexa). Dropped: the COB FirePrimary only slept 3 s.

pelvis, legs, ground, base, lbody, rbody, launcher, emit =
	piece('pelvis', 'legs', 'ground', 'base', 'lbody', 'rbody', 'launcher', 'emit')
rfthigh, rfleg, rffoot, lfthigh, lfleg, lffoot = piece('rfthigh', 'rfleg', 'rffoot', 'lfthigh', 'lfleg', 'lffoot')
rmthigh, rmleg, rmfoot, lmthigh, lmleg, lmfoot = piece('rmthigh', 'rmleg', 'rmfoot', 'lmthigh', 'lmleg', 'lmfoot')
rbthigh, rbleg, rbfoot, lbthigh, lbleg, lbfoot = piece('rbthigh', 'rbleg', 'rbfoot', 'lbthigh', 'lbleg', 'lbfoot')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
local hexaReady = walk.Hexa()

local rad = math.rad
local SIG_AIM = 2
local RESTORE_DELAY = 10000       -- COB: S1
local COB_ANGLE = 2 * math.pi / 65536

local opened = false              -- COB S0: launcher up, weapon may aim
local current, desired, busy = 1, 1, false   -- COB RequestState: 0 = open, 1 = closed

local function Open()             -- COB activatescr
	Sleep(240)
	Move(lbody, x_axis, 4.375, 7.415)        -- COB x moves are negated in Lua
	Move(rbody, x_axis, -4.0, 6.78)
	Sleep(590)
	Turn(launcher, x_axis, rad(39.73), rad(136.98))
	Sleep(290)
	Turn(launcher, x_axis, rad(93.52), rad(244.50))
	Sleep(220)
	Turn(launcher, x_axis, rad(105.47), rad(54.33))
	Sleep(220)
	Turn(launcher, x_axis, rad(102.30), rad(18.61))
	Sleep(170)
	Turn(launcher, x_axis, rad(98.44), rad(22.75))
	Sleep(340)
	opened = true
end

local function Close()            -- COB deactivatescr
	opened = false
	Move(lbody, x_axis, 4.375)
	Move(rbody, x_axis, -4.0)
	Turn(launcher, x_axis, rad(98.44))
	Turn(launcher, x_axis, rad(92.11), rad(31.64))
	Sleep(200)
	Turn(launcher, x_axis, rad(70.66), rad(107.22))
	Sleep(200)
	Turn(launcher, x_axis, rad(17.23), rad(267.19))
	Sleep(200)
	Turn(launcher, x_axis, rad(0.35), rad(84.38))
	Sleep(200)
	Move(lbody, x_axis, 0, 21.875)
	Move(rbody, x_axis, 0, 20.0)
	Sleep(400)
end

local function RequestState(req)
	desired = req
	if busy then return end
	busy = true
	while desired ~= current do
		if desired == 0 then
			Open(); current = 0
		else
			Close(); current = 1
		end
	end
	busy = false
end

function script.Create()
	hexaReady()
	StartThread(SmokeUnit, {base})
end

local function RestoreAfterDelay()
	SetSignalMask(SIG_AIM)
	Sleep(RESTORE_DELAY)
	SetSignalMask(0)
	RequestState(1)
end

function script.AimWeapon(num, heading, pitch)
	StartThread(RequestState, 0)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	while not opened do
		Sleep(200)
	end
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return base                   -- COB has no AimFromPrimary: piece 0
end

function script.QueryWeapon(num)
	return emit
end

function script.SweetSpot(num)
	return base
end

local function Rock(x, z)         -- COB HitByWeapon: tilt 500 * hit direction (COB angle units), settle at 30 deg/s
	Turn(base, z_axis, -500 * x * COB_ANGLE, rad(105))
	Turn(base, x_axis, 500 * z * COB_ANGLE, rad(105))
	WaitForTurn(base, z_axis)
	WaitForTurn(base, x_axis)
	Turn(base, z_axis, 0, rad(30))
	Turn(base, x_axis, 0, rad(30))
end

function script.HitByWeapon(x, z, weaponDefID, damage)
	StartThread(Rock, x, z)       -- not thread-wrapped by the gadget
end

local LEGS = {rfthigh, rfleg, rffoot, lfthigh, lfleg, lffoot, rmthigh, rmleg, rmfoot,
	lmthigh, lmleg, lmfoot, rbthigh, rbleg, rbfoot, lbthigh, lbleg, lbfoot}
local HULL = {base, launcher, lbody, rbody}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	for _, p in ipairs(HULL) do Explode(p, SFX.NONE) end
	if severity <= 25 then
		for _, p in ipairs(LEGS) do Explode(p, SFX.NONE) end
		return 1
	elseif severity <= 50 then
		for _, p in ipairs(LEGS) do Explode(p, SFX.FALL) end
		return 2
	end
	for _, p in ipairs(LEGS) do Explode(p, SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT) end
	return 3
end
