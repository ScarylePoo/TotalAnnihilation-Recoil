-- From Splinter Faction (LuaRules/Gadgets/unit_friendly_fire_removal.lua). TA:Recoil changes marked.
function gadget:GetInfo()
	return {
		name      = "Friendly Fire Removal",
		desc      = "No damage to your own or allied units, unless the weapon has customparams.friendlyfire = \"true\"",
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

-- TA:Recoil: allied teams too (SF blocked only the attacker's own team), so there is no friendly fire at all.
-- It covers everything with an attacker: weapons, D-Gun, death explosions and self-destructs (the dying unit is the
-- attacker), so your own exploding buildings no longer hurt your or your allies' units.
local spAreTeamsAllied = Spring.AreTeamsAllied

local allowFF = {}
for weaponDefID, wd in pairs(WeaponDefs) do
	if wd.customParams and wd.customParams.friendlyfire == "true" then
		allowFF[weaponDefID] = true
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
