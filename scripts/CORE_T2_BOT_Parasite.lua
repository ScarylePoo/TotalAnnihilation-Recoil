-- Parasite (CORE_T2_BOT_Parasite): Lua unit script for the remodelled spy walker (standard biped skeleton).
-- Ported from TA's CORE_T2_BOT_Parasite.COB: it has no weapon; the COB only walked, smoked when damaged and died.
-- SweetSpot = head (the body); corpse types are the COB's. Its Killed exploded `head` once per old leg piece (a
-- compiler quirk); here the body explodes once with the COB's flags. The old walk (toes/heels) is replaced by the
-- shared one (scripts/headers/walk.lua).

pelvis, legs, rthigh, rleg, rfoot, lthigh, lleg, lfoot = piece('pelvis', 'legs', 'rthigh', 'rleg', 'rfoot', 'lthigh', 'lleg', 'lfoot')
ground, head = piece('ground', 'head')

include "smokeunit.lua"
local walk = include("headers/walk.lua")
walk.Biped()

function script.Create()
	StartThread(SmokeUnit, {head})
end

function script.SweetSpot(num)
	return head                   -- COB: piece 0
end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth * 100
	if severity <= 25 then
		Explode(head, SFX.NONE)
		return 1
	elseif severity <= 50 then
		Explode(head, SFX.SHATTER)
		return 2
	elseif severity <= 99 then
		Explode(head, SFX.SHATTER)
		return 2
	end
	Explode(head, SFX.SHATTER + SFX.EXPLODE_ON_HIT)
	return 2
end
