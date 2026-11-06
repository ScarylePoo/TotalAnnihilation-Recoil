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
	-- TA units did not regenerate; the engine's default is 10 HP/s after idleTime. Units without the tag get none.
	if ud.idleautoheal == nil then
		ud.idleautoheal = 0
	end
	if COMMANDERS[name] then
		ud.customparams = ud.customparams or {}
		ud.customparams.iscommander = 1
	end
end

-- Air repair pads: the engine ignores isairbase, luarules/gadgets/unit_air_pads.lua reads this.
for name, ud in pairs(UnitDefs) do
	if ud.isairbase then
		ud.customparams = ud.customparams or {}
		ud.customparams.isairbase = 1
	end
end
