--------------------------------------------------------------------------------
-- Unit definition post-processing: see gamedata/alldefs_post.lua (all game tweaks live there). Don't add any here.
--------------------------------------------------------------------------------

-- Keep the engine's own post-processing (description cleanup, piece trail CEGs).
VFS.Include('gamedata/unitdefs_post.lua', nil, VFS.BASE)

VFS.Include('gamedata/alldefs_post.lua')

for name, ud in pairs(UnitDefs) do
	UnitDef_Post(name, ud)
end
