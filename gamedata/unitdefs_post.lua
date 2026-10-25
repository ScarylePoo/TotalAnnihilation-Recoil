--------------------------------------------------------------------------------
-- Unit definition post-processing
--------------------------------------------------------------------------------

-- Keep the engine's own post-processing (description cleanup, piece trail CEGs).
VFS.Include('gamedata/unitdefs_post.lua', nil, VFS.BASE)

-- Commanders: read by luarules/gadgets/game_com_ends.lua (game end modes
-- "commander" and "comends"). Decoy commanders are deliberately not listed.
local COMMANDERS = {
	arm_commander  = true,
	core_commander = true,
}

for name, ud in pairs(UnitDefs) do
	if COMMANDERS[name] then
		ud.customparams = ud.customparams or {}
		ud.customparams.iscommander = 1
	end
end
