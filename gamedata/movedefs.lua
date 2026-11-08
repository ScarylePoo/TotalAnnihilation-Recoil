-- Movement classes: defined in gamedata/movedefs_classes.lua (laid out like Splinter Faction). Tags a class leaves
-- out get the defaults in movedefs_tags.lua, then movedefs_post.lua runs.

local moveDefs = VFS.Include("gamedata/movedefs_classes.lua")
local tagList  = VFS.Include("gamedata/movedefs_tags.lua")

for _, md in pairs(moveDefs) do
	for tagName, tagVal in pairs(tagList) do
		tagName = string.lower(tagName)
		if md[tagName] == nil and tagVal ~= 0 then
			md[tagName] = tagVal
		end
	end
end

local postProcFile = "gamedata/movedefs_post.lua"
if VFS.FileExists(postProcFile) then
	MoveDefs = moveDefs  -- global for the post script
	VFS.Include(postProcFile)
	MoveDefs = nil
end

return moveDefs
