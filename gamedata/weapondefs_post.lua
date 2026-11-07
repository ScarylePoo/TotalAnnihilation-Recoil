--------------------------------------------------------------------------------
-- Weapon definition post-processing: see gamedata/alldefs_post.lua (all game tweaks live there). Don't add any here.
--------------------------------------------------------------------------------

-- The engine's own post-processor turns TA weapon tags (rendertype, lineofsight,
-- ballistic, dropped, vlaunch, beamlaser, color/color2 ...) into Spring weapon
-- types and rgbColor, fills craterAreaOfEffect, and removes the legacy tags so
-- the engine does not warn about them. It is maintained with the engine, so use
-- it instead of an old copy. It must run first: WeaponDef_Post relies on weapontype.
VFS.Include('gamedata/weapondefs_post.lua', nil, VFS.BASE)

VFS.Include('gamedata/alldefs_post.lua')

for name, wd in pairs(WeaponDefs) do
	if type(wd) == 'table' then
		WeaponDef_Post(name, wd)
	end
end

-- death explosion effects per unit (needs the unit defs, loaded before the weapon defs)
DeathExplosions(DEFS.unitDefs, WeaponDefs)
