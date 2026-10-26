-- Infiltrator (ARM_T2_BOT_Infiltrator): Lua unit script for the remodelled spy walker (standard biped skeleton).
-- Ported from TA's ARM_T2_BOT_Infiltrator.COB: Activate/Deactivate queue RequestState(0/1); activatescr slides the
-- hood forward 4.1 elmo and tips it 41 deg over the head and the buttguard back 2.9 elmo / -41 deg over the tail;
-- deactivatescr reverses it. Speeds, sleeps, SweetSpot (torso) and the death table are the COB's. The old walk (which
-- also nodded head, tail and plates) is replaced by the shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
groundx2, torso, butt, head, backshield, buttguard, hood =
	piece('groundx2', 'torso', 'butt', 'head', 'backshield', 'buttguard', 'hood')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad

local function activatescr()
	Move(buttguard, z_axis, 0)
	Move(buttguard, z_axis, -2.875, 3.734)
	Move(hood, z_axis, 0)
	Move(hood, z_axis, 4.125, 5.357)
	Turn(buttguard, x_axis, rad(0))
	Turn(buttguard, x_axis, rad(-40.65), rad(52.8))
	Turn(hood, x_axis, rad(0))
	Turn(hood, x_axis, rad(41.39), rad(53.76))
	Sleep(770)
	Sleep(20)
end

local function deactivatescr()
	Move(buttguard, z_axis, -2.875)
	Move(buttguard, z_axis, 0, 5.044)
	Move(hood, z_axis, 4.125)
	Move(hood, z_axis, 0, 7.237)
	Turn(buttguard, x_axis, rad(-40.65))
	Turn(buttguard, x_axis, rad(0), rad(71.32))
	Turn(hood, x_axis, rad(41.39))
	Turn(hood, x_axis, rad(0), rad(72.62))
	Sleep(570)
	Sleep(10)
end
-- COB RequestState: one worker runs the open/close scripts until the requested state stops changing
local wanted, current, busy = 1, 1, false
local function RequestState(state)
	wanted = state
	if busy then return end
	busy = true
	while wanted ~= current do
		current = wanted
		if current == 0 then activatescr() else deactivatescr() end
	end
	busy = false
end

function script.Create()
	StartThread(SmokeUnit, {torso})
end

function script.Activate()
	StartThread(RequestState, 0)
end

function script.Deactivate()
	StartThread(RequestState, 1)
end

function script.SweetSpot(num)
	return torso                  -- COB: piece 0
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({backshield, butt, buttguard, head, hood, lfoot, lleg, lthigh, rfoot, rleg, rthigh, torso}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({backshield}, SFX.SHATTER)
		Blow({butt, buttguard, head, hood, torso}, SFX.NONE)
		Blow({lfoot, lleg, lthigh, rfoot, rleg, rthigh}, SFX.FALL)
		return 2
	elseif severity <= 99 then
		Blow({backshield}, SFX.SHATTER)
		Blow({butt, buttguard, head, hood, torso}, SFX.NONE)
		Blow({lfoot, lleg, lthigh, rfoot, rleg, rthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		return 3
	end
	Blow({backshield}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	Blow({butt, buttguard, head, hood, torso}, SFX.NONE)
	Blow({lfoot, lleg, lthigh, rfoot, rleg, rthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	return 3
end
