-- Hammer (ARM_T1_BOT_Hammer): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T1_BOT_Hammer.COB: the gun clamshells (upcase2 / locase) open with the same keyframes and
-- speeds before it may fire (Go) and close again after the restore delay (Stop), driven by the same RequestState
-- queue; torso 90 deg/s, guns 45 deg/s, alternating cannons with 5 elmo recoil, same death table and corpse types.
-- The walk is the shared one (scripts/headers/walk.lua); the 1998 muzzle-flash show/hide of the firepoints is gone
-- (the weapon's CEG is the flash), the pieces stay as emit points. COB axis conventions are converted: COB negates
-- turn-z and move-x destinations (Recoil CobInstance.h "COBWTF"); this script uses none of those axes.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, torso, canbase, lcannon, lfirept, rcannon, rfirept, upcase2, locase =
	piece('ground', 'torso', 'canbase', 'lcannon', 'lfirept', 'rcannon', 'rfirept', 'upcase2', 'locase')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_AIM = 2
local restoreDelay = 3000        -- COB: SetMaxReloadTime -> reload * 2
local deployed = false           -- COB static 3: shells open, guns ready
local gun = 0                    -- COB static 4: 0 = right cannon fires next

-- ---------------------------------------------------------------- open / close (COB Go / Stop, same keyframes)
local function SetFirepoints()
	Move(rfirept, y_axis, -0.75); Move(rfirept, z_axis, 0.525)
	Move(lfirept, y_axis, -0.75); Move(lfirept, z_axis, 0.525)
end

local function Go()
	if deployed then return end
	Move(lcannon, y_axis, 0); Move(lcannon, z_axis, 0)
	Move(rcannon, y_axis, 0); Move(rcannon, z_axis, 0)
	Move(locase, y_axis, 0); Move(locase, z_axis, 0)
	-- (COB also issues `move locase z -1.85 speed 0` here: a zero-speed anim never advances, so it is omitted)
	SetFirepoints()
	Turn(upcase2, x_axis, 0)
	Turn(upcase2, x_axis, rad(-43), rad(110.97))
	Turn(locase, x_axis, 0)
	Turn(locase, x_axis, rad(61), rad(155.96))
	Sleep(394)
	Move(upcase2, z_axis, -10.95, 220)
	Turn(upcase2, x_axis, rad(-47), rad(63.98))
	Move(locase, z_axis, -10.95, 220)
	Turn(locase, x_axis, rad(64), rad(63.98))
	Sleep(50)
	Turn(upcase2, x_axis, rad(-121), rad(1373.66))
	Turn(locase, x_axis, rad(139), rad(1373.66))
	Sleep(55)
	Turn(upcase2, x_axis, rad(-45), rad(902.78))
	Turn(locase, x_axis, rad(63), rad(902.78))
	Sleep(85)
	Turn(upcase2, x_axis, rad(-19), rad(753.82))
	Turn(locase, x_axis, rad(37), rad(753.82))
	Sleep(35)
	Turn(upcase2, x_axis, rad(-47), rad(2886.3))
	Turn(locase, x_axis, rad(64), rad(2886.3))
	Sleep(20)
	deployed = true
end

local function Stop()
	if not deployed then return end
	deployed = false
	Move(lcannon, y_axis, 0); Move(lcannon, z_axis, 0)
	Move(rcannon, y_axis, 0); Move(rcannon, z_axis, 0)
	Move(upcase2, z_axis, -10.95)
	Move(upcase2, z_axis, 2.375, 55)
	Move(locase, y_axis, 0)
	Move(locase, z_axis, -1.85)
	SetFirepoints()
	Turn(upcase2, x_axis, rad(-47.1))
	Turn(locase, x_axis, rad(61.52))
	Sleep(229)
	Move(upcase2, z_axis, 4.25, 35)
	Turn(upcase2, x_axis, rad(-41), rad(110.97))
	Sleep(54)
	Move(upcase2, z_axis, 0, 500)
	Move(locase, z_axis, 0, 220)
	Turn(upcase2, x_axis, 0, rad(4838.82))
	Turn(locase, x_axis, 0, rad(7237.23))
	Sleep(14)
end

-- COB RequestState: one worker runs Go/Stop until the requested state stops changing
local wanted, current, busy = 1, 1, false
local function RequestState(state)
	wanted = state
	if busy then return end
	busy = true
	while wanted ~= current do
		current = wanted
		if current == 0 then Go() else Stop() end
	end
	busy = false
end

-- ---------------------------------------------------------------- weapon
function script.Create()
	local wd = UnitDefs[unitDefID].weapons[1]
	if wd and WeaponDefs[wd.weaponDef] then
		restoreDelay = WeaponDefs[wd.weaponDef].reload * 2000
	end
	StartThread(SmokeUnit, {torso, pelvis})
end

local function RestoreAfterDelay()
	Sleep(restoreDelay)
	SetSignalMask(0)
	Turn(torso, y_axis, 0, rad(90))
	Turn(canbase, x_axis, 0, rad(45))
	StartThread(RequestState, 1)
end

function script.AimWeapon(num, heading, pitch)
	StartThread(RequestState, 0)
	Signal(SIG_AIM)
	SetSignalMask(SIG_AIM)
	while not deployed do
		Sleep(350)
	end
	Turn(torso, y_axis, heading, rad(90))
	Turn(canbase, x_axis, -pitch, rad(45))
	WaitForTurn(torso, y_axis)
	WaitForTurn(canbase, x_axis)
	StartThread(RestoreAfterDelay)
	return true
end

function script.AimFromWeapon(num)
	return pelvis                 -- COB: piece 0
end

function script.QueryWeapon(num)
	return (gun == 0) and rfirept or lfirept
end

function script.FireWeapon(num)
	if gun == 0 then
		gun = 1
		Move(rcannon, z_axis, -5, 62.5)
		Sleep(100)
		Move(rcannon, z_axis, 0, 10)
	else
		gun = 0
		Move(lcannon, z_axis, -5, 62.5)
		Sleep(100)
		Move(lcannon, z_axis, 0, 10)
	end
end

function script.SweetSpot(num)
	return pelvis                 -- COB: piece 0
end

local DEATH = {ground, lfirept, lfoot, lleg, locase, lthigh, pelvis, rfirept, rfoot, rleg, upcase2, rthigh}

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.NONE) end
		Explode(canbase, SFX.NONE); Explode(torso, SFX.NONE)
		Explode(lcannon, SFX.NONE); Explode(rcannon, SFX.NONE)
		return 1
	elseif severity <= 50 then
		for _, p in ipairs(DEATH) do Explode(p, SFX.FALL) end
		Explode(canbase, SFX.NONE); Explode(torso, SFX.NONE)
		Explode(lcannon, SFX.SHATTER); Explode(rcannon, SFX.SHATTER)
		return 2
	end
	local f = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	for _, p in ipairs(DEATH) do Explode(p, f) end
	Explode(canbase, SFX.NONE); Explode(torso, SFX.NONE)
	local g = SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0)
	Explode(lcannon, g); Explode(rcannon, g)
	return 3
end
