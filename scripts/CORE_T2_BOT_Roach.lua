-- Roach (CORE_T2_BOT_Roach): Lua unit script for the remodelled hexapod crawling bomb (shared six-leg skeleton).
-- Ported from TA's CORE_T2_BOT_Roach.COB: no weapon (kamikaze, handled by the engine), smoke when damaged, same death
-- table: the twelve old stub legs' entries go to the eighteen new leg pieces, the two that SHATTERed (lega6, legb6)
-- to the rear shins. The walk is the shared hexapod tripod gait (scripts/headers/walk.lua, walk.Hexa).

pelvis, legs, base = piece('pelvis', 'legs', 'base')
rfthigh, rfleg, rffoot, lfthigh, lfleg, lffoot = piece('rfthigh', 'rfleg', 'rffoot', 'lfthigh', 'lfleg', 'lffoot')
rmthigh, rmleg, rmfoot, lmthigh, lmleg, lmfoot = piece('rmthigh', 'rmleg', 'rmfoot', 'lmthigh', 'lmleg', 'lmfoot')
rbthigh, rbleg, rbfoot, lbthigh, lbleg, lbfoot = piece('rbthigh', 'rbleg', 'rbfoot', 'lbthigh', 'lbleg', 'lbfoot')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
local hexaReady = walk.Hexa({minStep = 0.2})

function script.Create()
	hexaReady()
	StartThread(SmokeUnit, {base})
end

function script.SweetSpot(num)
	return base
end

local LEGS = {rfthigh, rffoot, lfthigh, lffoot, rmthigh, rmleg, rmfoot, lmthigh, lmleg, lmfoot,
	rbthigh, rbfoot, lbthigh, lbfoot, rfleg, lfleg}
local SHATTER = {rbleg, lbleg}    -- COB: lega6 / legb6

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		return 1
	end
	Explode(base, SFX.NONE)
	if severity <= 50 then
		for _, p in ipairs(LEGS) do Explode(p, SFX.FALL) end
		for _, p in ipairs(SHATTER) do Explode(p, SFX.SHATTER) end
		return 2
	end
	for _, p in ipairs(LEGS) do Explode(p, SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT) end
	for _, p in ipairs(SHATTER) do Explode(p, SFX.SHATTER + ((severity > 99) and SFX.EXPLODE_ON_HIT or 0)) end
	return 2
end
