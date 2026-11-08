-- From Splinter Faction (LuaRules/Gadgets/unit_friendly_fire_removal.lua). TA:Recoil changes marked.
function gadget:GetInfo()
	return {
		name      = "Friendly Fire Removal",
		desc      = "No friendly fire from ordinary weapons; death explosions, self-destructs, the D-Gun and nukes still hurt everyone",
		author    = "",
		date      = "",
		license   = "GNU GPL, v2 or later",
		layer     = 0,
		enabled   = true
	}
end

if not gadgetHandler:IsSyncedCode() then
	return
end

-- TA:Recoil: allied teams too (SF blocked only the attacker's own team). User decision: ordinary weapons do no
-- friendly fire, but these still hurt everyone, as in TA (blowing up your own base was part of the game):
--   unit and building death explosions and self-destructs (every unit's explodeAs / selfDestructAs weapon,
--     mines and crawling bombs included)
--   the D-Gun (weapon type DGun)
--   nukes (missiles an anti-nuke can shoot down: Retaliator, Silencer, also Stunner/Neutron)
--   any weapon with customparams.friendlyfire = "true"
local spAreTeamsAllied = Spring.AreTeamsAllied

local allowFF = {}
for weaponDefID, wd in pairs(WeaponDefs) do
	local cp = wd.customParams or {}
	if cp.friendlyfire == "true" or cp.deathexplosion or wd.type == "DGun" or (wd.targetable and wd.targetable ~= 0) then
		allowFF[weaponDefID] = true
	end
end
for _, ud in pairs(UnitDefs) do
	for _, name in ipairs({ ud.deathExplosion, ud.selfDExplosion }) do
		local wd = name and WeaponDefNames[string.lower(name)]
		if wd then
			allowFF[wd.id] = true
		end
	end
end

function gadget:UnitPreDamaged(unitID, unitDefID, unitTeam, damage, paralyzer, weaponDefID, projectileID, attackerID, attackerDefID, attackerTeam)
	if attackerTeam and (unitTeam == attackerTeam or spAreTeamsAllied(unitTeam, attackerTeam)) then
		if weaponDefID and allowFF[weaponDefID] then
			return damage
		end
		return 0
	end
	return damage
end
