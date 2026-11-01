-- Voyeur (CORE_T2_BOT_Voyeur): Lua unit script for the remodelled radar walker (standard biped skeleton).
-- Ported from TA's CORE_T2_BOT_Voyeur.COB: Activate spins the radar plate (dish1) about y at 100 deg/s, Deactivate
-- turns it back to 0; SweetSpot = body; the death table and corpse types are the COB's (old thigh1/leg1/foot1 = the
-- right leg). The old walk (which also rolled the body) is replaced by the shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, body, arm1, arm2, dish1 = piece('ground', 'body', 'arm1', 'arm2', 'dish1')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

local rad = math.rad
local SIG_ACT = 2

function script.Create()
	StartThread(SmokeUnit, {body})
end

function script.Activate()
	Signal(SIG_ACT)
	Spin(dish1, y_axis, rad(100))
end

local function DeactivateThread()
	Signal(SIG_ACT)
	SetSignalMask(SIG_ACT)
	Turn(dish1, y_axis, 0, rad(100))
	WaitForTurn(dish1, y_axis)
end

function script.Deactivate()
	StartThread(DeactivateThread)
end

function script.SweetSpot(num)
	return body                   -- COB: piece 0
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({arm1, arm2, body, dish1, rfoot, lfoot, rleg, lleg, rthigh, lthigh}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({arm1, arm2, rfoot, lfoot, rleg, lleg, rthigh, lthigh}, SFX.FALL)
		Blow({body}, SFX.NONE)
		Blow({dish1}, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Blow({arm1, arm2, rfoot, lfoot, rleg, lleg, rthigh, lthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		Blow({body}, SFX.NONE)
		Blow({dish1}, SFX.SHATTER)
		return 3
	end
	Blow({arm1, arm2, rfoot, lfoot, rleg, lleg, rthigh, lthigh}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	Blow({body}, SFX.NONE)
	Blow({dish1}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 3
end
