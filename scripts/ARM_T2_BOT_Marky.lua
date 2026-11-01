-- Marky (ARM_T2_BOT_Marky): Lua unit script for the remodelled walker (standard biped skeleton).
-- Ported from TA's ARM_T2_BOT_Marky.COB: Activate spins the two radar vanes about x at 100 deg/s in opposite
-- directions, Deactivate turns them back to 0; SweetSpot = head, same death table and corpse types (the old shins
-- Rshin/Lshin are the skeleton's rleg/lleg). The old walk (walk2/stand) is replaced by the shared one.

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
base, head, ldish, rdish = piece('base', 'head', 'ldish', 'rdish')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_ACT = 2

function script.Create()
	StartThread(SmokeUnit, {head})
end

function script.Activate()
	Signal(SIG_ACT)
	Spin(rdish, x_axis, rad(100))
	Spin(ldish, x_axis, rad(-100))
end

local function DeactivateThread()
	Signal(SIG_ACT)
	SetSignalMask(SIG_ACT)
	Turn(rdish, x_axis, 0, rad(100))
	Turn(ldish, x_axis, 0, rad(100))
	WaitForTurn(rdish, x_axis)
	WaitForTurn(ldish, x_axis)
end

function script.Deactivate()
	StartThread(DeactivateThread)
end

function script.SweetSpot(num)
	return head                   -- COB: piece 0
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({base, head, ldish, lfoot, lleg, lthigh, rdish, rfoot, rleg, rthigh}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({base, ldish, lfoot, lleg, lthigh, rdish, rfoot, rleg, rthigh}, SFX.FALL)
		Blow({head}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({base, ldish, lfoot, lleg, lthigh, rdish, rfoot, rleg, rthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({head}, SFX.SHATTER)
		return 3
	end
	Blow({base, ldish, lfoot, lleg, lthigh, rdish, rfoot, rleg, rthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({head}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
