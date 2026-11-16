-- Core Galactic Gate: a static mission objective (ported from TA's corgate.bos: smoke when damaged, Killed).
include "smokeunit.lua"

local base, arms, platform, disha, dishb = piece('base', 'arms', 'platform', 'disha', 'dishb')

function script.Create()
	StartThread(SmokeUnit, {base})
end

function script.Killed(recentDamage, maxHealth)
	local severity = recentDamage / maxHealth
	if severity <= 0.25 then
		return 1                -- leave a wreck
	end
	local fly = SFX.FALL + SFX.SMOKE + SFX.FIRE + SFX.EXPLODE_ON_HIT
	if severity <= 0.50 then
		fly = SFX.FALL
	end
	Explode(arms, SFX.SHATTER)
	Explode(platform, fly)
	Explode(disha, fly)
	Explode(dishb, fly)
	if severity <= 0.50 then
		return 2                -- leave a heap
	end
	return 3                    -- leave nothing
end
