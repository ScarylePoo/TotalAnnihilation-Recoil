--------------------------------------------------------------------------------
-- Unit definition post-processing
--------------------------------------------------------------------------------

-- Keep the engine's own post-processing (description cleanup, piece trail CEGs).
VFS.Include('gamedata/unitdefs_post.lua', nil, VFS.BASE)

-- Build lists: a builder's FBI names its list (BuildList=<name>;), the lists
-- are in gamedata/unitdefs_pre.lua as Shared.<name>. The engine's own check
-- for unknown build options runs before this file, so it is repeated here.
for name, ud in pairs(UnitDefs) do
	local listName = ud.buildlist
	if listName then
		local list = Shared[listName]
		if type(list) ~= 'table' then
			Spring.Log('unitdefs_post', LOG.ERROR, name .. ': unknown BuildList "' .. tostring(listName) .. '"')
		else
			local options = {}
			for i = 1, #list do
				local option = list[i]:lower()
				if UnitDefs[option] then
					options[#options + 1] = option
				else
					Spring.Log('unitdefs_post', LOG.ERROR, name .. ': ' .. listName .. ' lists unknown unit "' .. list[i] .. '"')
				end
			end
			ud.buildoptions = options
		end
		ud.buildlist = nil
	end
end

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
