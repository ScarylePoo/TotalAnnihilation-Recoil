-- Invader (ARM_T2_BOT_Invader): Lua unit script for the remodelled crawling bomb (standard QUAD skeleton).
-- Ported from TA's ARM_T2_BOT_Invader.COB: it only walks and dies (the weapon is the death explosion). The four TA
-- legs map to the quad skeleton's shins (leg1 = left back, leg2 = right back, leg3 = right front, leg4 = left front)
-- for the death table; corpse types are the COB's. SweetSpot is the shell (the COB used leg1, piece 0). The old walk
-- is replaced by the shared quad walk (scripts/headers/walk.lua).

pelvis, legs = piece('pelvis', 'legs')
rfthigh, rfleg, rffoot, lfthigh, lfleg, lffoot = piece('rfthigh', 'rfleg', 'rffoot', 'lfthigh', 'lfleg', 'lffoot')
rbthigh, rbleg, rbfoot, lbthigh, lbleg, lbfoot = piece('rbthigh', 'rbleg', 'rbfoot', 'lbthigh', 'lbleg', 'lbfoot')
base = piece('base')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Quad()

function script.Create()
	StartThread(SmokeUnit, {base})
end

function script.SweetSpot(num)
	return base
end

local function Blow(list, f) for _, p in ipairs(list) do Explode(p, f) end end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Blow({base, lbleg, rbleg, rfleg, lfleg}, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Blow({base}, SFX.NONE)
		Blow({lbleg}, SFX.SHATTER)
		Blow({rbleg, rfleg, lfleg}, SFX.FALL)
		return 2
	elseif severity <= 99 then
		Blow({base}, SFX.NONE)
		Blow({lbleg}, SFX.SHATTER)
		Blow({rbleg, rfleg, lfleg}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
		return 3
	end
	Blow({base}, SFX.NONE)
	Blow({lbleg}, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	Blow({rbleg, rfleg, lfleg}, SFX.EXPLODE_ON_HIT + SFX.FALL + SFX.SMOKE + SFX.FIRE)
	return 3
end
